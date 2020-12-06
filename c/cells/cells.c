#include <stdlib.h>
#include <stdio.h>


/**
 * ############################################################################
 * ##                            AUTOMATA CODE                               ##
 * ############################################################################
 */

#define MAX_NEIGHBOURS 8
#define DEAD 0
#define ALIVE 1

float random_spawn = 0.5;

typedef struct Automata_s
{
	 int **now;
	 int **future;
	 int width;
	 int height;
	 int max_hp;
	 float revival_probability[MAX_NEIGHBOURS];
	 int bleed[MAX_NEIGHBOURS];
} Automata;

Automata* create_automata(int width, int height)
{
	 Automata *a = (Automata*)malloc(sizeof(Automata));
	 a->width = width;
	 a->height = height;
	 a->now = (int**)malloc(width*sizeof(int*));
	 a->future = (int**)malloc(width*sizeof(int*));
	 for(int x=0; x<width; x++)
	 {
			a->now[x] = (int*)malloc(height*sizeof(int));
			a->future[x] = (int*)malloc(height*sizeof(int));
	 }
	 
	 return a;
}

void clear_automata(Automata *a)
{
	 for(int x=0;x<a->width;x++)
	 {
			for(int y=0;y<a->height;y++)
			{
				 a->now[x][y] = 0;
			}
	 }	 
}

void randomize_automata(Automata *a)
{
	 for(int x=0;x<a->width;x++)
	 {
			for(int y=0;y<a->height;y++)
			{
				 a->now[x][y] = (float)rand()/(float)RAND_MAX<random_spawn?a->max_hp:0;
			}
	 }	 
}


int get_cell_state(Automata *a, int x, int y)
{
	 if(x<0||x>=a->width||y<0||y>=a->height) return DEAD;
	 if(a->now[x][y]>0) return ALIVE;
	 return DEAD;
}


int neighbour_count(Automata *a, int x, int y)
{
	 if(x<0||x>=a->width||y<0||y>=a->height) return 0;
	 int n_count=0;
	 for(int dx=-1;dx<=1;dx++)
	 {
			for(int dy=-1;dy<=1;dy++)
			{
				 if(dx==0&&dy==0) continue;
				 if(get_cell_state(a,x+dx,y+dy)==ALIVE) n_count++;
			}			
	 }	 
	 return n_count;
}


void tick(Automata *a)
{
	 for(int x=0; x<a->width; x++)
	 {
			for(int y=0; y<a->height; y++)
			{
				 int nc = neighbour_count(a,x,y);
				 if(a->now[x][y])
				 {
						a->future[x][y]=a->now[x][y]-a->bleed[nc];
						if(a->future[x][y]<0) a->future[x][y]=0;
				 }
				 else if((float)rand()/(float)RAND_MAX<a->revival_probability[nc])
				 {
						a->future[x][y] = a->max_hp;
				 }
			}
	 }
	 int **tmp = a->now;
	 a->now = a->future;
	 a->future = tmp;
}

/**
 * ############################################################################
 * ##                        CONFIG PROCESSING                               ##
 * ############################################################################
 */

void load_config(Automata *a, const char* cfg_file_name)
{
	 printf("Loading config from file %s \n", cfg_file_name);
	 FILE *config = fopen(cfg_file_name, "r");
	 fscanf(config, "%d\n",&(a->max_hp));
	 fscanf(config, "%f %f %f %f %f %f %f %f\n",
				 a->revival_probability,
				 a->revival_probability+1,
				 a->revival_probability+2,
				 a->revival_probability+3,
				 a->revival_probability+4,
				 a->revival_probability+5,
				 a->revival_probability+6,
				 a->revival_probability+7);
	 fscanf(config, "%d %d %d %d %d %d %d %d\n",
				 a->bleed,
				 a->bleed+1,
				 a->bleed+2,
				 a->bleed+3,
				 a->bleed+4,
				 a->bleed+5,
				 a->bleed+6,
				 a->bleed+7);
	 fclose(config);
	 printf("Max hp = %d\n", a->max_hp);
	 printf("Revival probabilities = ");
	 for(int i=0; i<8; i++)
	 {
			printf("%f ",a->revival_probability[i]);
	 }
	 printf("\n");
	 printf("Bleed values = ");
	 for(int i=0; i<8; i++)
	 {
			printf("%d ",a->bleed[i]);
	 }
	 printf("\n");

}

void load_pattern(Automata *a, const char *pattern_file_name)
{
	 printf("Loading pattern from file %s \n", pattern_file_name);
	 FILE *pattern = fopen(pattern_file_name, "r");
	 int x,y,hp;
	 while(fscanf(pattern,"[%d,%d]=%d",&x,&y,&hp)==3)
	 {
			a->now[x][y]=hp;
			//printf("[%d,%d]=%d\n",x,y,hp);
			while(fgetc(pattern)!='\n'){}
	 }
	 fclose(pattern);
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
int pause = 1;
int show_lifeforce = 0;

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

void test_user_interface()
{
	 printf("Testing user interface. \n");
	 init_user_interface();
	 SDL_SetRenderDrawColor( renderer, 255, 0, 0, 255 );
	 SDL_RenderClear( renderer );
	 SDL_Rect r;
	 r.x = 50;
	 r.y = 50;
	 r.w = 50;
	 r.h = 50;
	 SDL_SetRenderDrawColor( renderer, 0, 0, 255, 255 );
	 SDL_RenderFillRect(renderer, &r);
	 SDL_RenderPresent(renderer);
	 SDL_Delay(2000);
	 cleanup_user_interface();
}

void draw_automata(Automata *a)
{
	 int cell_width = SCREEN_WIDTH/a->width;
	 int cell_height = SCREEN_HEIGHT/a->height;
	 SDL_Rect cell_rect;
	 cell_rect.w = cell_width;
	 cell_rect.h = cell_height;
	 for(int x=0;x<a->width;x++)
	 {
			for(int y=0;y<a->height;y++)
			{
				 cell_rect.x=x*cell_width;
				 cell_rect.y=y*cell_height;
				 if(show_lifeforce==2)
				 {
						int saturation = (int)(255*((float)a->now[x][y]/(float)a->max_hp));
						SDL_SetRenderDrawColor( renderer, 0, saturation, 0, 255 );
				 }
				 else if(show_lifeforce==1)
				 {
						if(a->now[x][y]==a->max_hp)
						{
							 SDL_SetRenderDrawColor( renderer, 0, 255, 0, 255 );
						}
						else if(a->now[x][y]==0)
						{
							 SDL_SetRenderDrawColor( renderer, 0, 0, 0, 255 );
						}
						else
						{
							 SDL_SetRenderDrawColor( renderer, 255, 0, 0, 255 );
						}
				 }
				 else
				 {			
						if(a->now[x][y])
							{
								 SDL_SetRenderDrawColor( renderer, 0, 255, 0, 255 );
							}
						else
							{
								 SDL_SetRenderDrawColor( renderer, 0, 0, 0, 255 );
							}
				 }
				 SDL_RenderFillRect(renderer, &cell_rect);
			}
	 }
	 SDL_RenderPresent(renderer);
}

int check_user_input(Automata *a)
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
					case SDLK_l:
						show_lifeforce++;
						if(show_lifeforce>2) show_lifeforce=0;
						break;
					case SDLK_p:
						pause = !pause;
						break;
					case SDLK_r:
						if(pause) randomize_automata(a);
						break;
					case SDLK_COMMA:
						random_spawn-=0.01;
						printf("Random spawn probability is %f\n", random_spawn);
						break;
					case SDLK_PERIOD:
						random_spawn+=0.01;
						printf("Random spawn probability is %f\n", random_spawn);
						break;
				 }
				 break;
			}
			
	 }
	 return 0;
}


void main_loop(Automata *a)
{
	 draw_automata(a);
	 check_user_input(a);
	 if(!pause) tick(a);
	 SDL_Delay(100);
}


/**
 * ############################################################################
 * ##                                  MAIN                                  ##
 * ############################################################################
 */


int main(int argc, char** argv)
{
	 Automata *a = create_automata(100,100);
	 load_config(a,argv[1]);
	 if(argc==3) load_pattern(a,argv[2]);
	 init_user_interface();
	 while(running)
	 {
			main_loop(a);
	 }
	 cleanup_user_interface();
}

