use std::env;
use std::fs;
use std::error::Error;

pub fn run(config: Config) -> Result<(), Box<dyn Error>> {
    let contents = fs::read_to_string(&config.filename)?;
    println!("Searching for {} in {}", config.query, config.filename);
    println!("Contents of text file :\n{}", contents);
    Ok(())
}

pub struct Config{
    query: String,
    filename: String,
}

impl Config{
    pub fn parse_command_line() -> Result<Config, &'static str> { 
        let args: Vec<String> = env::args().collect();
        if args.len() < 3 {
            return Err("Not enough arguments");
        }

        let query = args[1].clone();
        let filename = args[2].clone();

        Ok(Config {query, filename})
    }
}

