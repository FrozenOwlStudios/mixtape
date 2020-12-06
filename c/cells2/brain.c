#include <stdlib.h>
#include <stdio.h>


/**
 * ############################################################################
 * ##                            AUTOMATA CODE                               ##
 * ############################################################################
 */


#define A_S 100
#define DEAD 0
#define DYING 1
#define ALIVE 2
#define RANDOMIZE_LIMIT 3

int **now;
int **ftr;

void init()
{
	 now = (int**)malloc(sizeof(int*)*A_S);
	 ftr = (int**)malloc(sizeof(int*)*A_S);
	 for(int x=0; x<A_S; x++)
	 {
			now[x] = (int*)malloc(sizeof(int)*A_S);
			ftr[x] = (int*)malloc(sizeof(int)*A_S);
			for(int y=0; y<A_S; y++)
			{
				 now[x][y] = DEAD;
				 ftr[x][y] = DEAD;
			}
	 }
}

int n_count(int x, int y)
{
	 int n_c=0;
	 for(int dx=-1; dx<=1; dx++)
	 {
			for(int dy=0; dy<=1; dy++)
			{
				 if((dx==0&&dy==0)||
						x+dx<0||x+dx>=A_S||
						y+dy<0||y+dy>=A_S)
				 {
						continue;
				 }
				 if(now[x+dx][y+dy]==ALIVE) n_c++;
			}
	 }
	 return n_c;
}


void tick()
{
	 for(int x=0; x<A_S; x++)
	 {
			for(int y=0; y<A_S; y++)
			{
				 switch(now[x][y])
				 {
					case DEAD: 
						ftr[x][y]=n_count(x,y)==2?ALIVE:DEAD;
						break;
					case ALIVE:
						ftr[x][y]=DYING;
						break;
					case DYING:
						ftr[x][y]=DEAD;
				 }				 
			}		
	 }
	 int **tmp = now;
	 now = ftr;
	 ftr = tmp;
}

void randomize()
{
	 for(int x=0; x<A_S; x++)
	 {
			for(int y=0; y<A_S; y++)
			{
				 now[x][y] = rand()%RANDOMIZE_LIMIT;
			}
	 }
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
	 int cell_width = SCREEN_WIDTH/A_S;
	 int cell_height = SCREEN_HEIGHT/A_S;
	 SDL_Rect cell_rect;
	 cell_rect.w = cell_width;
	 cell_rect.h = cell_height;
	 for(int x=0;x<A_S;x++)
	 {
			for(int y=0;y<A_S;y++)
			{
				 cell_rect.x=x*cell_width;
				 cell_rect.y=y*cell_height;
				 switch(now[x][y])
				 {
					case ALIVE:
						SDL_SetRenderDrawColor( renderer, 0, 255, 0, 255 );
						break;
					case DYING:
						SDL_SetRenderDrawColor( renderer, 0, 0, 255, 255 );
						break;
					case DEAD:
						SDL_SetRenderDrawColor( renderer, 0, 0, 0, 255 );
				 }
				 SDL_RenderFillRect(renderer, &cell_rect);
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
						if(pause) randomize();
						break;
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
	 init();
	 randomize();
	 init_user_interface();
	 while(running) main_loop();
	 cleanup_user_interface();
	 return 0;
}
