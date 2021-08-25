use ggez;
use ggez::{graphics, event};
use ggez::{GameResult, GameError, ContextBuilder, Context};
use ggez::graphics::{Color};
use ggez::event::EventHandler;
use ggez::mint::Vector2;


const RACKET_HEIGHT:f32 = 100.0;
const RACKET_WIDTH:f32 = 20.0;
const RACKET_HEIGHT_HALF:f32 = RACKET_HEIGHT*0.5;
const RACKET_WIDTH_HALF:f32 = RACKET_WIDTH*0.5;


fn main() -> GameResult {
    let (mut context, event_loop) = ContextBuilder::new("Zrzynka", "Kolektyw").build()?;
    graphics::set_window_title(&context, "Zrzynka");
    let mut game = PongGame::new();
    event::run(context, event_loop, game);
}



struct Racket{
    position: Vector2<f32>,
    size: Vector2<f32>,
    color: Color,
}

impl Racket{
    pub fn new(x: f32, y: f32, w: f32, h: f32, color: Color) -> Racket{
        Racket{
            position: Vector2{x, y},
            size: Vector2{x:w, y:h},
            color
        }
    }

    pub fn get_mesh(&self, context: &mut Context)-> graphics::Mesh{
        let rect = graphics::Rect::new(self.position.x,
                                       self.position.y,
                                       self.size.x,
                                       self.size.y);
        graphics::Mesh::new_rectangle(context,graphics::DrawMode::fill(),
                                      rect,self.color).unwrap()
        
    }
}


struct PongGame{
    left_player: Racket,
}


impl PongGame{
    pub fn new() -> PongGame{
        PongGame{
            left_player: Racket::new(RACKET_WIDTH_HALF, RACKET_HEIGHT_HALF,
                                     RACKET_WIDTH, RACKET_HEIGHT,
                                     Color::YELLOW)
        }
    }
}

impl EventHandler<GameError> for PongGame{
    fn update(&mut self, context: &mut Context) -> Result<(),GameError> {
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
        graphics::present(context)
    }
}
