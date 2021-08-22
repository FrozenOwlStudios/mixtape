use std::process;
use minigrep::Config;

fn main() {

    let config = Config::parse_command_line().unwrap_or_else(|err|{
        println!("{}",err);
        process::exit(1);
    });

    if let Err(err) = minigrep::run(config){
        println!("{}", err);
        process::exit(1);
    }


}

