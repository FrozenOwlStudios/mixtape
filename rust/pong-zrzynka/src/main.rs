use ggez;
use ggez::{graphics, event, timer};
use ggez::{GameResult, GameError, ContextBuilder, Context};
use ggez::graphics::{Color};
use ggez::event::{EventHandler, KeyCode, KeyMods};
use ggez::mint::Vector2;
use std::ops::Range;

const RACKET_HEIGHT:f32 = 100.0;
const RACKET_WIDTH:f32 = 20.0;
const RACKET_HEIGHT_HALF:f32 = RACKET_HEIGHT*0.5;
const RACKET_WIDTH_HALF:f32 = RACKET_WIDTH*0.5;
const RACKET_ACCELERATION:f32 = 9.0;
const FRICTION:f32 = 0.1;
const BALL_SIZE:f32 = 20.0;
const BALL_SIZE_HALF:f32 = BALL_SIZE/2.0;
const BALL_SERVE_VELOCITY_MAX:f32 = 100.0;
const MINIMUM_VELOCITY:f32 = 0.005;


fn main() -> GameResult {
    let (mut context, event_loop) = ContextBuilder::new("Zrzynka", "Kolektyw").build()?;
    graphics::set_window_title(&context, "Zrzynka");
    let game = PongGame::new(&mut context);
    event::run(context, event_loop, game);
}



struct Racket{
    position: Vector2<f32>,
    velocity: Vector2<f32>,
    acceleration: Vector2<f32>,
    size: Vector2<f32>,
    color: Color,
}

impl Racket{
    pub fn new(x: f32, y: f32, w: f32, h: f32, color: Color) -> Racket{
        Racket{
            position: Vector2{x, y},
            size: Vector2{x:w, y:h},
            color,
            velocity: Vector2{x:0.0, y:0.0},
            acceleration: Vector2{x:0.0, y:0.0}
        }
    }

    pub fn get_mesh(&self, context: &mut Context)-> graphics::Mesh{
        let (_, screen_height) = graphics::drawable_size(context);
        let x = self.position.x-RACKET_WIDTH_HALF;
        // We must transform position from (0,0) at bottom left to (0,0) top left.
        let y = screen_height - (self.position.y+RACKET_HEIGHT_HALF);
        let rect = graphics::Rect::new(x, y, self.size.x, self.size.y);
        graphics::Mesh::new_rectangle(context,graphics::DrawMode::fill(),
                                      rect,self.color).unwrap()
        
    }

    pub fn update(&mut self, dt: f32, context: &Context){
        self.check_border_collisions(context);
        self.apply_acceleration(dt);
    }

    fn apply_acceleration(&mut self, dt: f32){
        self.position.x += self.velocity.x*dt + self.acceleration.x*dt*dt/2.0;
        self.position.y += self.velocity.y*dt + self.acceleration.y*dt*dt/2.0;
        self.velocity.x += self.acceleration.x*dt - self.velocity.x*FRICTION*dt;
        self.velocity.y += self.acceleration.y*dt - self.velocity.y*FRICTION*dt;
        if self.velocity.x.abs() < MINIMUM_VELOCITY {
            self.velocity.x = 0.0;
        }
        if self.velocity.y.abs() < MINIMUM_VELOCITY {
            self.velocity.y = 0.0;
        }
        
    }

    fn check_border_collisions(&mut self, context: &Context){
        let (_, screen_height) = graphics::drawable_size(context);
        if self.position.y - RACKET_HEIGHT_HALF <= 0.0 ||
            self.position.y + RACKET_HEIGHT_HALF >= screen_height{
            self.velocity.y = 0.0-self.velocity.y;
        }
    }
}


struct Ball{
    position: Vector2<f32>,
    velocity: Vector2<f32>,
    acceleration: Vector2<f32>,
    size: Vector2<f32>,
}

impl Ball{
    pub fn new(x: f32, y: f32, size: f32) -> Ball{
        Ball{
            position: Vector2{x, y},
            size: Vector2{x:size, y:size},
            velocity: Vector2{x:0.0, y:0.0},
            acceleration: Vector2{x:0.0, y:0.0}
        }
    }

    pub fn get_mesh(&self, context: &mut Context)-> graphics::Mesh{
        let (_, screen_height) = graphics::drawable_size(context);
        let x = self.position.x-BALL_SIZE_HALF;
        // We must transform position from (0,0) at bottom left to (0,0) top left.
        let y = screen_height - (self.position.y+BALL_SIZE_HALF);
        let rect = graphics::Rect::new(x, y, self.size.x, self.size.y);
        graphics::Mesh::new_rectangle(context,graphics::DrawMode::fill(),
                                      rect,Color::BLUE).unwrap()
        
    }

    pub fn update(&mut self, dt: f32, context: &Context, left_racket: &Racket,
                  right_racket: &Racket){
        self.check_border_collisions(dt, context);
        self.apply_acceleration(dt);
        self.check_racket_collisions(dt, context, left_racket);
        self.check_racket_collisions(dt, context, right_racket);

    }

    fn apply_acceleration(&mut self, dt: f32){
        self.position.x += self.velocity.x*dt + self.acceleration.x*dt*dt/2.0;
        self.position.y += self.velocity.y*dt + self.acceleration.y*dt*dt/2.0;
        self.velocity.x += self.acceleration.x*dt - self.velocity.x*FRICTION*dt;
        self.velocity.y += self.acceleration.y*dt - self.velocity.y*FRICTION*dt;
        if self.velocity.x.abs() < MINIMUM_VELOCITY {
            self.velocity.x = 0.0;
        }
        if self.velocity.y.abs() < MINIMUM_VELOCITY {
            self.velocity.y = 0.0;
        }
    }

    fn check_border_collisions(&mut self, dt: f32, context: &Context){
        let (screen_width, screen_height) = graphics::drawable_size(context);
        if self.position.y - BALL_SIZE_HALF <= 0.0 ||
            self.position.y + BALL_SIZE_HALF >= screen_height{
            self.velocity.y = 0.0-self.velocity.y;
        }
        if self.position.x - BALL_SIZE_HALF <= 0.0 ||
            self.position.x + BALL_SIZE_HALF >= screen_width{
            self.velocity.x = 0.0-self.velocity.x;
        }
    }

    fn check_racket_collisions(&mut self, dt: f32, context: &Context,racket: &Racket ){
        let x_range = Range{start: racket.position.x-RACKET_WIDTH,
        end: racket.position.x+RACKET_WIDTH};
        let y_range = Range{start: racket.position.y-RACKET_HEIGHT,
        end: racket.position.y+RACKET_HEIGHT};
        if (x_range.contains(&(self.position.x+BALL_SIZE)) &&
            y_range.contains(&(self.position.y+BALL_SIZE)))||
            (x_range.contains(&(self.position.x-BALL_SIZE)) &&
            y_range.contains(&(self.position.y-BALL_SIZE))){
            self.velocity.y = 0.0-self.velocity.y;
            self.velocity.x = 0.0-self.velocity.x;
        }
    }

    pub fn serve(&mut self){
        self.velocity.x = 100.0;
        self.velocity.y = 150.0;
    }
}


struct PongGame{
    left_player: Racket,
    right_player: Racket,
    ball: Ball,
}


impl PongGame{
    pub fn new(context: &mut Context) -> PongGame{
        let (screen_width, screen_height) = graphics::drawable_size(context);
        PongGame{
            left_player: Racket::new(RACKET_WIDTH_HALF,
                                     screen_height*0.5,
                                     RACKET_WIDTH,
                                     RACKET_HEIGHT,
                                     Color::YELLOW),
            right_player: Racket::new(screen_width-RACKET_WIDTH_HALF,
                                      screen_height*0.5,
                                      RACKET_WIDTH,
                                      RACKET_HEIGHT,
                                      Color::GREEN),
            ball: Ball::new(screen_width*0.5,
                            screen_height*0.5,
                            BALL_SIZE)
        }
    }
}

impl EventHandler<GameError> for PongGame{
    fn update(&mut self, context: &mut Context) -> Result<(),GameError> {
        let dt = timer::delta(&context).as_secs_f32();
        self.left_player.update(dt, context);
        self.right_player.update(dt, context);
        self.ball.update(dt, context, &self.left_player, &self.right_player);
        Ok(())
    }

    fn draw(&mut self, context: &mut Context) -> Result<(),GameError> {
        graphics::clear(context, Color::BLACK);
        //let rect = graphics::Rect::new(100.0, 100.0, 20.0, 20.0);
        //let mesh = graphics::Mesh::new_rectangle(context,
        //                                         graphics::DrawMode::fill(),
        //                                         rect,
        //                                         Color::YELLOW).unwrap();
        let mesh = self.left_player.get_mesh(context);
        graphics::draw(context, &mesh, graphics::DrawParam::default())?;
        let mesh = self.right_player.get_mesh(context);
        graphics::draw(context, &mesh, graphics::DrawParam::default())?;
        let mesh = self.ball.get_mesh(context);
        graphics::draw(context, &mesh, graphics::DrawParam::default())?;
        graphics::present(context)
    }

    fn key_down_event(&mut self, context: &mut Context, key: KeyCode, _: KeyMods, _: bool) {
        match key {
            KeyCode::Escape => {
                    println!("Terminating!");
                    event::quit(context);
            }
            KeyCode::W => {
                self.left_player.acceleration.y = RACKET_ACCELERATION;
            }
            KeyCode::S => {
                self.left_player.acceleration.y = 0.0-RACKET_ACCELERATION;
            }
            KeyCode::O => {
                self.right_player.acceleration.y = RACKET_ACCELERATION;
            }
            KeyCode::L => {
                self.right_player.acceleration.y = 0.0-RACKET_ACCELERATION;
            }
            KeyCode::Space =>{
                self.ball.serve();
            }
            _ => (),
        }
    }

    fn key_up_event(&mut self, context: &mut Context, key: KeyCode, _: KeyMods){
        match key {
            KeyCode::W => {
                self.left_player.acceleration.y = 0.0;
            }
            KeyCode::S => {
                self.left_player.acceleration.y = 0.0;
            }
            KeyCode::O => {
                self.right_player.acceleration.y = 0.0;
            }
            KeyCode::L => {
                self.right_player.acceleration.y = 0.0;
            }
            _ => (),
        }
    }
}
