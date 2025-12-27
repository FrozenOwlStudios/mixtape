#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <math.h>

//==============================================================================
//                              BASIC STRUCTURES
//==============================================================================

/* Discrete cartesian coordinates*/
typedef struct
{
    int x;
    int y;
} CartDisc;

/* Continous cartesian coordinates */
typedef struct
{
    float x;
    float y;
} CartCont;

CartCont cart_disc_to_cont(CartDisc disc)
{
    float fx = (float)disc.x;
    float fy = (float)disc.y;
    CartCont cont = {.x = fx, .y = fy};
    return cont;
}

CartDisc cart_cont_to_disc(CartCont disc)
{
    int ix = (int)(disc.x + 0.5);
    int iy = (int)(disc.y + 0.5);
    CartDisc cont = {.x = ix, .y = iy};
    return cont;
}

CartCont mult(CartCont a, double v)
{
    CartCont res = {.x = a.x * v, .y = a.y * v};
    return res;
}

typedef struct
{
    CartDisc explosion; /* Explosion coordinates*/
    int start_frame;    /* when to launch (frame index) */
    int burst_count;    /* particles created on explosion */
    float speed;        /* base speed of particles */
    int start_y;        /* initial rocket Y (TERM_H-1 for ground level) */
} FireworkConfig;

//==============================================================================
//                                CONFIG
//==============================================================================

#define TERM_W 100
#define TERM_H 30

#define MS_PER_FRAME 33     /* ~30 FPS */
#define REDRAW_FULL_FRAME 1 /* 1 = redraw full frame */

#define MAX_PARTICLES 900
#define GRAVITY 0.045f
#define DRAG 0.992f

#define FIREWORK_COUNT 4
static FireworkConfig FIREWORKS[FIREWORK_COUNT] = {
    {.explosion = {20, 10}, 10, 120, 1.35f, TERM_H - 1},
    {.explosion = {55, 8}, 45, 160, 1.60f, TERM_H - 1},
    {.explosion = {80, 12}, 80, 140, 1.45f, TERM_H - 1},
    {.explosion = {35, 6}, 115, 180, 1.70f, TERM_H - 1},
};

//==============================================================================
//                              HELPER FUNCTIONS
//==============================================================================
typedef uint32_t time_ms;

inline void sleep_ms(int ms) { usleep((time_ms)ms * 1000); }

//==============================================================================
//                                  RNG
//==============================================================================
// *Really* minimal PCG32 code / (c) 2014 M.E. O'Neill / pcg-random.org
// Licensed under Apache License 2.0 (NO WARRANTY, etc. see website)

typedef struct
{
    uint64_t state;
    uint64_t inc;
} pcg32_random_t;

pcg32_random_t global_rng = {0, 0};

uint32_t pcg32_random_r(pcg32_random_t *rng)
{
    uint64_t oldstate = rng->state;
    // Advance internal state
    rng->state = oldstate * 6364136223846793005ULL + (rng->inc | 1);
    // Calculate output function (XSH RR), uses old state for max ILP
    uint32_t xorshifted = ((oldstate >> 18u) ^ oldstate) >> 27u;
    uint32_t rot = oldstate >> 59u;
    return (xorshifted >> rot) | (xorshifted << ((-rot) & 31));
}

static float frand01(pcg32_random_t *rng)
{
    return (pcg32_random_r(rng) & 0xFFFFFF) / (float)0x1000000;
}

static float frand(float a, float b, pcg32_random_t *rng)
{
    return a + (b - a) * frand01(rng);
}

//==============================================================================
//                              PARTICLES
//==============================================================================
#define GLYPH_COUNT 3
char PARTICLE_GLYPHS[GLYPH_COUNT] = {'*', '+', 'o'};

typedef struct
{
    CartCont position;
    CartCont velocity;
    float lifetime_s;
    char glyph;
    int active; /* Bool like (0-false 1-true)*/
} Particle;

static Particle particles[MAX_PARTICLES];

static int particle_alloc()
{
    for (int i = 0; i < MAX_PARTICLES; i++)
    {
        if (!particles[i].active)
            return i;
    }
    return -1;
}

static void particle_spawn_burst(CartDisc pos, int count, float base_speed)
{
    /* Mixture of ring + random sparks */
    for (int i = 0; i < count; i++)
    {
        int idx = particle_alloc();
        if (idx < 0)
            break;

        float ang = frand(0.0f, 6.2831853f, &global_rng);
        float sp = base_speed * frand(0.55f, 1.15f, &global_rng);

        /* Some particles are in a tighter ring */
        if ((i % 5) == 0)
            sp = base_speed * frand(0.95f, 1.05f, &global_rng);

        CartCont velocity = {.x = sp * (float)cos(ang), .y = sp * (float)sin(ang)};
        particles[idx].position = cart_disc_to_cont(pos);
        particles[idx].velocity = velocity;
        particles[idx].lifetime_s = frand(0.9f, 1.7f, &global_rng); /* lifetime in seconds */
        particles[idx].glyph = PARTICLE_GLYPHS[i % GLYPH_COUNT];
        particles[idx].active = 1;
    }
}

void particle_update(Particle *particles)
{
}

//==============================================================================
//                               FIREWORK
//==============================================================================
typedef enum
{
    FW_WAITING,
    FW_ROCKET,
    FW_BURST,
    FW_DONE
} FireworkState;

typedef struct
{
    FireworkConfig cfg;
    FireworkState st;
    int launched_frame;
    CartCont position;
    float rocket_vy;
    int exploded;
} Firework;

void firework_spawn(Firework *fws)
{
    for (int i = 0; i < FIREWORK_COUNT; i++)
    {
        fws[i].cfg = FIREWORKS[i];
        fws[i].st = FW_WAITING;
        fws[i].launched_frame = -1;
        CartDisc start_pos = {.x = fws[i].cfg.explosion.x, .y = fws[i].cfg.start_y};
        fws[i].position = cart_disc_to_cont(start_pos);
        fws[i].rocket_vy = -0.75f - frand(0.0f, 0.3f, &global_rng); /* upward */
        fws[i].exploded = 0;
    }
}

//==============================================================================
//                               GRAPHICS
//==============================================================================
void term_hide_cursor(void) { printf("\x1b[?25l"); }
void term_show_cursor(void) { printf("\x1b[?25h"); }
void term_clear(void) { printf("\x1b[2J"); }
void term_home(void) { printf("\x1b[H"); }

char canvas[TERM_H][TERM_W + 1];

void canvas_clear()
{
    for (int y = 0; y < TERM_H; y++)
    {
        for (int x = 0; x < TERM_W; x++)
            canvas[y][x] = ' ';
        canvas[y][TERM_W] = '\0';
    }
}

static void draw_frame(char canvas[TERM_H][TERM_W + 1])
{
    if (REDRAW_FULL_FRAME)
    {
        term_home();
    }

    for (int y = 0; y < TERM_H; y++)
    {
        fwrite(canvas[y], 1, TERM_W, stdout);
        fputc('\n', stdout);
    }
    fflush(stdout);
}

//==============================================================================
//                               MAIN
//==============================================================================

int main(void)
{
    /* Initialize fireworks */
    Firework fws[FIREWORK_COUNT];
    firework_spawn(fws);

    memset(particles, 0, sizeof(particles));

    term_hide_cursor();
    term_clear();
    term_home();

    const int total_frames = 220;
    for (int frame = 0; frame < total_frames; frame++)
    {

        /* Update fireworks */
        for (int i = 0; i < FIREWORK_COUNT; i++)
        {
            Firework *fw = &fws[i];

            if (fw->st == FW_DONE)
                continue;

            if (fw->st == FW_WAITING)
            {
                if (frame >= fw->cfg.start_frame)
                {
                    fw->st = FW_ROCKET;
                    fw->launched_frame = frame;
                    fw->rocket_vy = -0.85f - frand(0.0f, 0.35f, &global_rng);
                }
            }
            else if (fw->st == FW_ROCKET)
            {
                /* Move rocket upward */
                fw->position.x += fw->rocket_vy;
                fw->rocket_vy *= 0.995f;

                CartDisc pos = cart_cont_to_disc(fw->position);

                if (pos.y >= 0 && pos.y < TERM_H && pos.x >= 0 && pos.x < TERM_W)
                {
                    canvas[pos.y][pos.x] = '|';
                    if (pos.y + 1 < TERM_H)
                        canvas[pos.y + 1][pos.x] = '.';
                }

                /* Explode when reaching target or TTL runs out (remember higher is smaller number)*/
                if (fw->position.y <= fw->cfg.explosion.y || (frame - fw->launched_frame) > 80)
                {
                    fw->st = FW_BURST;
                }
            }
            else if (fw->st == FW_BURST)
            {
                if (!fw->exploded)
                {
                    fw->exploded = 1;
                    particle_spawn_burst(cart_cont_to_disc(fw->position), fw->cfg.burst_count, fw->cfg.speed);
                }
                fw->st = FW_DONE;
            }
        }

        /* Update particles */
        for (int i = 0; i < MAX_PARTICLES; i++)
        {
            if (!particles[i].active)
                continue;

            particles[i].velocity = mult(particles[i].velocity, DRAG);
            particles[i].velocity.y += GRAVITY;

            particles[i].position.x += particles[i].velocity.x;
            particles[i].position.y += particles[i].velocity.y;

            particles[i].lifetime_s -= MS_PER_FRAME / 1000.0f;

            CartDisc pos = cart_cont_to_disc(particles[i].position);

            if (particles[i].lifetime_s <= 0.0f || pos.x < 0 || pos.x >= TERM_W || pos.y < 0 || pos.y >= TERM_H)
            {
                particles[i].active = 0;
                continue;
            }

            /* Simple fade: later life uses '.' */
            char g = particles[i].glyph;
            if (particles[i].lifetime_s < 0.35f)
                g = '.';
            else if (particles[i].lifetime_s < 0.60f)
                g = '*';

            canvas[pos.y][pos.x] = g;
        }

        draw_frame(canvas);
        sleep_ms(MS_PER_FRAME);
    }

    term_clear();
    term_show_cursor();
    term_home();
    return 0;
}