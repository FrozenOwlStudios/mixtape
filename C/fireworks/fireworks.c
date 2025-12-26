#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

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

CartCont cart_disc_to_cont(CartDisc disc){
    float fx= (float)disc.x ;
    float fy = (float)disc.y;
    CartCont cont = {.x=fx, .y=fy};
    return cont;
}

CartDisc cart_cont_to_disc(CartCont disc){
    int ix= (int)disc.x ;
    int iy = (int)disc.y;
    CartDisc cont = {.x=ix, .y=iy};
    return cont;
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
inline void term_hide_cursor(void) { printf("\x1b[?25l"); }
inline void term_show_cursor(void) { printf("\x1b[?25h"); }
inline void term_clear(void) { printf("\x1b[2J"); }
inline void term_home(void) { printf("\x1b[H"); }

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

pcg32_random_t global_rng = {0,0};

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
char PARTICLE_GLYPHS[GLYPH_COUNT] = {'*','+','o'};

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

static void particle_spawn_burst(CartDisc pos, int count, float base_speed) {
  /* Mixture of ring + random sparks */
  for (int i = 0; i < count; i++) {
    int idx = alloc_particle();
    if (idx < 0) break;

    float ang = frand(0.0f, 6.2831853f, &global_rng);
    float sp  = base_speed * frand(0.55f, 1.15f, &global_rng);

    /* Some particles are in a tighter ring */
    if ((i % 5) == 0) sp = base_speed * frand(0.95f, 1.05f);

    CartCont velocity = {.x=sp * (float)cos(ang), .y=sp * (float)sin(ang)};
    particles[idx].position = cart_disc_to_cont(pos);
    particles[idx].velocity = velocity;
    particles[idx].lifetime_s = frand(0.9f, 1.7f, &global_rng); /* lifetime in ~seconds */
    particles[idx].glyph = PARTICLE_GLYPHS[i % GLYPH_COUNT];
    particles[idx].active = 1;
  }
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

//==============================================================================
//                               MAIN
//==============================================================================
int main()
{
    return 0;
}