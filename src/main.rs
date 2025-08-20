use rand::prelude::*;
use std::{env, time::Instant, usize};

fn main() {
    // Read in the length of the array to generate.
    let length = env::args()
        .nth(1)
        .expect("Missing positional argument for length")
        .parse::<usize>()
        .expect("Argument must be a valid non-negative integer");

    // Generate numbers
    let numbers = generate_numbers(length);

    // Call `radix_sort` with a timer around it.
    let start = Instant::now();
    let radix_sorted_numbers = radix_sort(numbers.clone());
    let duration = start.elapsed();

    // Check that the numbers are sorted.
    assert!(is_sorted(radix_sorted_numbers));

    // Print out how long the run took.
    println!("{}ns", duration.as_nanos());

    // Call `std_sort` with a timer around it.
    let start = Instant::now();
    let _ = std_sort(numbers);
    let duration = start.elapsed();

    // Print out how long the run took.
    println!("{}ns", duration.as_nanos());
}

fn generate_numbers(length: usize) -> Vec<u64> {
    let mut rng = rand::rng();
    let mut vec = Vec::with_capacity(length);

    for _ in 0..length {
        vec.push(rng.random());
    }

    vec
}

fn is_sorted(numbers: Vec<u64>) -> bool {
    for pair in numbers.windows(2) {
        if pair[0] > pair[1] {
            return false;
        }
    }

    true
}

fn radix_sort(mut numbers: Vec<u64>) -> Vec<u64> {
    let mut buckets: [Vec<u64>; 10] = std::array::from_fn(|_| Vec::with_capacity(numbers.len()));

    for place in 0..20 {
        // Drain numbers into buckets
        for number in numbers.drain(..) {
            buckets[digit_at(&number, place)].push(number);
        }

        // Drain the buckets back into numbers
        for bucket in buckets.iter_mut() {
            numbers.extend(bucket.drain(..))
        }
    }

    numbers
}

fn digit_at(number: &u64, place: u32) -> usize {
    ((number / 10_u64.pow(place)) % 10) as usize
}

fn std_sort(mut numbers: Vec<u64>) -> Vec<u64> {
    numbers.sort();
    numbers
}
