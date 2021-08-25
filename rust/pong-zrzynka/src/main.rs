use ggez;
use ggez::{graphics, event};
use ggez::{GameResult, GameError, ContextBuilder, Context};
use ggez::graphics::{Color};
use ggez::event::EventHandler;

fn main() -> GameResult {
    let (mut context, event_loop) = ContextBuilder::new("Zrzynka", "Kolektyw").build()?;
    graphics::set_window_title(&context, "Zrzynka");
    let mut game = PongGame::new();
    event::run(context, event_loop, game);
}


struct PongGame{
}


impl PongGame{
    pub fn new() -> PongGame{
        PongGame{}
    }
}

impl EventHandler<GameError> for PongGame{
    fn update(&mut self, _ctx: &mut Context) -> GameResult<()> {
        // Update code here...
        Ok(())
    }

    fn draw(&mut self, ctx: &mut Context) -> GameResult<()> {
        graphics::clear(ctx, Color::WHITE);
        // Draw code here...
        graphics::present(ctx)
    }
}
