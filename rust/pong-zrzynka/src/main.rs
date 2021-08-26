use ggez;
use ggez::{graphics, event, timer};
use ggez::{GameResult, GameError, ContextBuilder, Context};
use ggez::graphics::{Color};
use ggez::event::{EventHandler, KeyCode, KeyMods};
use ggez::mint::Vector2;


const RACKET_HEIGHT:f32 = 100.0;
const RACKET_WIDTH:f32 = 20.0;
const RACKET_HEIGHT_HALF:f32 = RACKET_HEIGHT*0.5;
const RACKET_WIDTH_HALF:f32 = RACKET_WIDTH*0.5;
const RACKET_ACCELERATION:f32 = 9.0;
const FRICTION:f32 = 0.1;


fn main() -> GameResult {
    let (mut context, event_loop) = ContextBuilder::new("Zrzynka", "Kolektyw").build()?;
    graphics::set_window_title(&context, "Zrzynka");
    let mut game = PongGame::new(&mut context);
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
        self.check_border_collisions(dt, context);
        self.apply_acceleration(dt);
    }

    fn apply_acceleration(&mut self, dt: f32){
        self.position.x += self.velocity.x*dt + self.acceleration.x*dt*dt/2.0;
        self.position.y += self.velocity.y*dt + self.acceleration.y*dt*dt/2.0;
        self.velocity.x += self.acceleration.x*dt - self.velocity.x*FRICTION*dt;
        self.velocity.y += self.acceleration.y*dt - self.velocity.y*FRICTION*dt;
    }

    fn check_border_collisions(&mut self, dt: f32, context: &Context){
        let (_, screen_height) = graphics::drawable_size(context);
        if self.position.y - RACKET_HEIGHT_HALF <= 0.0 ||
            self.position.y + RACKET_HEIGHT_HALF >= screen_height{
            self.velocity.y = 0.0-self.velocity.y;
        }
    }
}


struct PongGame{
    left_player: Racket,
    right_player: Racket,
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
                                      Color::GREEN)
        }
    }
}

impl EventHandler<GameError> for PongGame{
    fn update(&mut self, context: &mut Context) -> Result<(),GameError> {
        let dt = timer::delta(&context).as_secs_f32();
        self.left_player.update(dt, context);
        self.right_player.update(dt, context);
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
        graphics::draw(context, &mesh, graphics::DrawParam::default());
        let mesh = self.right_player.get_mesh(context);
        graphics::draw(context, &mesh, graphics::DrawParam::default());
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
