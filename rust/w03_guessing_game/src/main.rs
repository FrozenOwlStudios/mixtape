use std::io;
use std::cmp::Ordering;
use rand::Rng;

fn main() {
    println!("!!! Guess the number !!!");

    let secret_number = rand::thread_rng().gen_range(1, 101);

    loop{
        println!("Enter your guess: ");
        let mut guess = String::new();
        io::stdin().read_line(&mut guess).expect("Failed to read the line");
        let guess: u32 = match guess.trim().parse() {
            Ok(num) => num,
            Err(_) => {
                println!("Input must be a number.");
                continue;
            },
        };

        println!("You guessed {}.", guess);
        match guess.cmp(&secret_number){
            Ordering::Less => println!("Value to small."),
            Ordering::Greater => println!("Value to large."),
            Ordering::Equal => {
                println!("Congratulations you guessed correctly.");
                break;
            }
        }
    }
}
