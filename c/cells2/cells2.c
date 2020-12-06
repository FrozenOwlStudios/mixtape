#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <limits.h>

#define TRUE 1
#define FALSE 0

/**
 * ############################################################################
 * ##                       RANDOM NUMBER GENERATION                         ##
 * ############################################################################
 */
 
 
typedef unsigned long uint32;

#define N              (624)                 // length of state vector
#define M              (397)                 // a period parameter
#define K              (0x9908B0DFU)         // a magic constant
#define hiBit(u)       ((u) & 0x80000000U)   // mask all but highest   bit of u
#define loBit(u)       ((u) & 0x00000001U)   // mask all but lowest    bit of u
#define loBits(u)      ((u) & 0x7FFFFFFFU)   // mask     the highest   bit of u
#define mixBits(u, v)  (hiBit(u)|loBits(v))  // move hi bit of u to hi bit of v
#define MT_RAND_MAX ULONG_MAX

static uint32   state[N+1];     // state vector + 1 extra to not violate ANSI C
static uint32   *next;          // next random value is computed from here
static int      left = -1;      // can *next++ this many times before reloading

void seedMT(uint32 seed)
{
    register uint32 x = (seed | 1U) & 0xFFFFFFFFU, *s = state;
    register int    j;

    for(left=0, *s++=x, j=N; --j;
        *s++ = (x*=69069U) & 0xFFFFFFFFU);
}


uint32 reloadMT(void)
{
    register uint32 *p0=state, *p2=state+2, *pM=state+M, s0, s1;
    register int    j;

    if(left < -1)
        seedMT(4357U);

    left=N-1, next=state+1;

    for(s0=state[0], s1=state[1], j=N-M+1; --j; s0=s1, s1=*p2++)
        *p0++ = *pM++ ^ (mixBits(s0, s1) >> 1) ^ (loBit(s1) ? K : 0U);

    for(pM=state, j=M; --j; s0=s1, s1=*p2++)
        *p0++ = *pM++ ^ (mixBits(s0, s1) >> 1) ^ (loBit(s1) ? K : 0U);

    s1=state[0], *p0 = *pM ^ (mixBits(s0, s1) >> 1) ^ (loBit(s1) ? K : 0U);
    s1 ^= (s1 >> 11);
    s1 ^= (s1 <<  7) & 0x9D2C5680U;
    s1 ^= (s1 << 15) & 0xEFC60000U;
    return(s1 ^ (s1 >> 18));
}


uint32 randomMT(void)
{
    uint32 y;

    if(--left < 0)
        return(reloadMT());

    y  = *next++;
    y ^= (y >> 11);
    y ^= (y <<  7) & 0x9D2C5680U;
    y ^= (y << 15) & 0xEFC60000U;
    return(y ^ (y >> 18));
}

 
 
double rand_double()
{
	 return (double)randomMT()/(double)MT_RAND_MAX;
}

int rand_int(int min, int max)
{ 
	 if(max-min==1)return min+((int)randomMT()%2);
	 return min+(int)randomMT()%(max-min);
}


/**
 * ############################################################################
 * ##                            AUTOMATA CODE                               ##
 * ############################################################################
 */
#define A_SIZE 250
#define N_COUNT 8

int l_crowd_effect[N_COUNT+1];
int l_personal_effect[N_COUNT];
int d_crowd_effect[N_COUNT+1];
int d_personal_effect[N_COUNT];
int max_hp;
int active_treshold;
int **now;
int **ftr;

void initialize_automata()
{
	 now = (int**)malloc(sizeof(int*)*A_SIZE);
	 ftr = (int**)malloc(sizeof(int*)*A_SIZE);
	 for(int x=0; x<A_SIZE; x++){
			now[x] = (int*)malloc(sizeof(int)*A_SIZE);
			ftr[x] = (int*)malloc(sizeof(int)*A_SIZE);
	 }
}

void randomize_config()
{
	 max_hp = rand_int(10,200);
	 active_treshold = rand_int(5,max_hp);
	 int max_change = max_hp/2;
	 for(int i=0; i<N_COUNT; i++){
			l_crowd_effect[i] = rand_int(0-max_change,max_change);
			l_personal_effect[i] = rand_int(0-max_change,max_change);
			d_crowd_effect[i] = rand_int(0-max_change,max_change);
			d_personal_effect[i] = rand_int(0-max_change,max_change);
	 }
	 l_crowd_effect[N_COUNT] = rand_int(0-max_change,max_change);
	 d_crowd_effect[N_COUNT] = rand_int(0-max_change,max_change);
}

int cell_active(int x, int y)
{
	 if(x<0||x>=A_SIZE||y<0||y>=A_SIZE) return FALSE;
	 return now[x][y]>=active_treshold;
}

/*
 * Cell numbering convention
 * 
 * +---+---+---+
 * | 0 | 1 | 2 |
 * +---+---+---+
 * | 3 + X + 4 |
 * +---+---+---+
 * | 5 | 6 | 7 |
 * +---+---+---+
 */
int dx[] = {-1,0,1,-1,1,-1,0,1};
int dy[] = {1,1,1,0,0,-1,-1,-1};


int change_value(int x,int y)
{
	 int l = now[x][y]>0;
	 int n = 0;
	 int change = 0;
	 for(int i=0; i<N_COUNT; i++){
			if(cell_active(x+dx[i],y+dy[i])){
				 n++;
				 change+=l?l_personal_effect[i]:d_personal_effect[i];
			}
	 }
	 change+=l?l_crowd_effect[n]:d_crowd_effect[n];
	 return change;
}

void tick()
{
	 for(int x=0; x<A_SIZE; x++){
			for(int y=0; y<A_SIZE; y++){
				 ftr[x][y]=now[x][y]+change_value(x,y);
				 if(ftr[x][y]<0) ftr[x][y]=0;
				 if(ftr[x][y]>max_hp) ftr[x][y]=max_hp;
			}			
	 }
	 int **tmp=now;
	 now=ftr;
	 ftr=tmp;
}

void randomize_automata()
{
	 	 for(int x=0; x<A_SIZE; x++){
			for(int y=0; y<A_SIZE; y++){
				 now[x][y] = rand_int(0,max_hp);
			}
		 }
}

/**
 * ############################################################################
 * ##                        CONFIG PROCESSING                               ##
 * ############################################################################
 */

void save_config(const char* cfg_file_name)
{
	 printf("Writing config to file %s \n", cfg_file_name);
	 FILE *config = fopen(cfg_file_name, "w");
	 fprintf(config,"%d\n",max_hp);
	 fprintf(config,"%d\n",active_treshold);
	 for(int i=0; i<N_COUNT; i++){
			fprintf(config,"%d ",l_crowd_effect[i]);
	 }
	 fprintf(config,"%d\n",l_crowd_effect[N_COUNT]);
	 for(int i=0; i<N_COUNT-1; i++){
			fprintf(config,"%d ",l_personal_effect[i]);
	 }
	 fprintf(config,"%d\n",l_personal_effect[N_COUNT-1]);
	 for(int i=0; i<N_COUNT; i++){
			fprintf(config,"%d ",d_crowd_effect[i]);
	 }
	 fprintf(config,"%d\n",d_crowd_effect[N_COUNT]);
	 for(int i=0; i<N_COUNT-1; i++){
			fprintf(config,"%d ",d_personal_effect[i]);
	 }
	 fprintf(config,"%d\n",d_personal_effect[N_COUNT-1]);
	 fclose(config);
}

void load_config(const char* cfg_file_name)
{
	 printf("Loading config from file %s \n", cfg_file_name);
	 FILE *config = fopen(cfg_file_name, "r");
	 fscanf(config,"%d\n",&max_hp);
	 fscanf(config,"%d\n",&active_treshold);
	 for(int i=0; i<N_COUNT; i++){
			fscanf(config,"%d ",l_crowd_effect+i);
	 }
	 fscanf(config,"%d\n",l_crowd_effect+N_COUNT);
	 for(int i=0; i<N_COUNT-1; i++){
			fscanf(config,"%d ",l_personal_effect+i);
	 }
	 fscanf(config,"%d\n",l_personal_effect+N_COUNT-1);
	 for(int i=0; i<N_COUNT; i++){
			fscanf(config,"%d ",d_crowd_effect+i);
	 }
	 fscanf(config,"%d\n",d_crowd_effect+N_COUNT);
	 for(int i=0; i<N_COUNT-1; i++){
			fscanf(config,"%d ",d_personal_effect+i);
	 }
	 fscanf(config,"%d\n",d_personal_effect+N_COUNT-1);
	 fclose(config);
}


void print_config()
{
	 printf("CONFIG : \n");
	 printf("%d\n",max_hp);
	 printf("%d\n",active_treshold);
	 for(int i=0; i<N_COUNT; i++){
			printf("%d ",l_crowd_effect[i]);
	 }
	 printf("%d\n",l_crowd_effect[N_COUNT]);
	 for(int i=0; i<N_COUNT-1; i++){
			printf("%d ",l_personal_effect[i]);
	 }
	 printf("%d\n",l_personal_effect[N_COUNT-1]);
	 for(int i=0; i<N_COUNT; i++){
			printf("%d ",d_crowd_effect[i]);
	 }
	 printf("%d\n",d_crowd_effect[N_COUNT]);
	 for(int i=0; i<N_COUNT-1; i++){
			printf("%d ",d_personal_effect[i]);
	 }
	 printf("%d\n",d_personal_effect[N_COUNT-1]);
}


/**
 * ############################################################################
 * ##                           USER INTERFACE                               ##
 * ############################################################################
 */
#include <SDL2/SDL.h>

#define SCREEN_WIDTH 800
#define SCREEN_HEIGHT 800

SDL_Window* window = NULL;
SDL_Renderer* renderer = NULL;

int running = 1;
int pause = 0;
int show_lifeforce = 0;
int show_borders = 0;

void init_user_interface()
{
	 printf("Initializing user interface. \n");
	 if(SDL_Init(SDL_INIT_VIDEO)<0) 
	 {
			printf( "SDL could not initialize! SDL_Error: %s\n", SDL_GetError() );
			return;
	 }
	 window = SDL_CreateWindow( "Generalised Game of Life", SDL_WINDOWPOS_UNDEFINED,
															SDL_WINDOWPOS_UNDEFINED, SCREEN_WIDTH,
															SCREEN_HEIGHT, SDL_WINDOW_SHOWN );
	 if( window == NULL ) 
	 {
			printf( "Window could not be created! SDL_Error: %s\n", SDL_GetError() ); 
	 }
	 
	 renderer =  SDL_CreateRenderer( window, -1, SDL_RENDERER_ACCELERATED);
	 if( renderer == NULL ) 
	 {
			printf( "Renderer could not be created! SDL_Error: %s\n", SDL_GetError() ); 
	 }
	 
	 printf("User interface initialized. \n");

}

void cleanup_user_interface()
{
	 printf("Cleanining up user interface. \n");
	 SDL_DestroyWindow( window );
	 SDL_Quit();
	 printf("User interface cleaned up. \n");
}

void draw_automata()
{
	 int cell_width = SCREEN_WIDTH/A_SIZE;
	 int cell_height = SCREEN_HEIGHT/A_SIZE;
	 SDL_Rect cell_rect;
	 cell_rect.w = cell_width;
	 cell_rect.h = cell_height;
	 for(int x=0;x<A_SIZE;x++)
	 {
			for(int y=0;y<A_SIZE;y++)
			{
				 cell_rect.x=x*cell_width;
				 cell_rect.y=y*cell_height;
				 int saturation = (int)(255*((float)now[x][y]/(float)max_hp));
				 SDL_SetRenderDrawColor( renderer, 0, 0, saturation, 255 );
				 SDL_RenderFillRect(renderer, &cell_rect);
				 if(show_borders){
						SDL_SetRenderDrawColor( renderer, 255, 255, 255, 255 );
						SDL_RenderDrawRect(renderer, &cell_rect);
				 }
				 
			}
	 }
	 SDL_RenderPresent(renderer);
}

int check_user_input()
{
	 SDL_Event event;
	 while( SDL_PollEvent( &event ) != 0 )
	 {
			switch (event.type)
		  {
			 case SDL_QUIT:
				 running = 0;
				 break;
			 case SDL_KEYDOWN:
				 switch(event.key.keysym.sym)
				 {
					case SDLK_ESCAPE:
						running = 0;
						break;
					case SDLK_p:
						pause = !pause;
						break;
					case SDLK_r:
						if(pause) randomize_automata();
						break;
					case SDLK_s:
						save_config("config.txt");
						break;
					case SDLK_b:
						show_borders=!show_borders;
				 }
				 break;
			}
			
	 }
	 return 0;
}

void main_loop()
{
	 draw_automata();
	 check_user_input();
	 if(!pause) tick();
	 SDL_Delay(100);
}


/**
 * ############################################################################
 * ##                                  MAIN                                  ##
 * ############################################################################
 */

int main(int argc, char **argv)
{
	 seedMT(clock());
	 initialize_automata();
	 if(argc==2){
			load_config(argv[1]);
	 }else{
			randomize_config();
	 }			
	 print_config();
	 randomize_automata();
	 init_user_interface();
	 while(running) main_loop();
	 cleanup_user_interface();
	 return 0;
}
