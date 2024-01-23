//$
const COLOR_PALETTE : &str = "21 12 4 100 111 95 75 100 165 126 80 100 148 140 108 100 153 148 138 100 201 163 107 100 213 193 150 100 195 178 161 100 135 102 67 100 111 95 75 100 165 126 80 100 148 140 108 100 153 148 138 100 201 163 107 100 213 193 150 100 195 178 161 100";
//&

use dygma_focus::prelude::*;
use anyhow::{anyhow, bail, Result};
use std::str::FromStr;

#[allow(dead_code)]
pub(crate) fn string_to_numerical_vec<T: FromStr>(str: &str) -> Result<Vec<T>>
where
    <T as FromStr>::Err: std::fmt::Debug,
{
    str.split_whitespace()
        .map(|part| part.parse::<T>().map_err(|e| anyhow!("{:?}", e)))
        .collect()
}

#[allow(dead_code)]
pub(crate) fn numerical_vec_to_string<T: ToString>(data: &[T]) -> String {
    data.iter()
        .map(|num| num.to_string())
        .collect::<Vec<String>>()
        .join(" ")
}

#[allow(dead_code)]
pub(crate) fn string_to_rgb_vec(str: &str) -> Result<Vec<RGB>> {
    str.split_whitespace()
        .collect::<Vec<&str>>()
        .chunks(3)
        .map(|chunk| {
            if chunk.len() != 3 {
                bail!("Invalid count, try RGBW instead");
            }
            let r = chunk[0].parse()?;
            let g = chunk[1].parse()?;
            let b = chunk[2].parse()?;

            Ok(RGB { r, g, b })
        })
        .collect()
}

#[allow(dead_code)]
pub(crate) fn rgb_vec_to_string(data: &[RGB]) -> String {
    data.iter()
        .map(|rgb| format!("{} {} {}", rgb.r, rgb.g, rgb.b))
        .collect::<Vec<String>>()
        .join(" ")
}

#[allow(dead_code)]
pub(crate) fn string_to_rgbw_vec(str: &str) -> Result<Vec<RGBW>> {
    str.split_whitespace()
        .collect::<Vec<&str>>()
        .chunks(4)
        .map(|chunk| {
            if chunk.len() != 4 {
                bail!("Invalid count, try RGB instead");
            }
            let r = chunk[0].parse()?;
            let g = chunk[1].parse()?;
            let b = chunk[2].parse()?;
            let w = chunk[3].parse()?;

            Ok(RGBW { r, g, b, w })
        })
        .collect()
}

#[allow(dead_code)]
pub(crate) fn rgbw_vec_to_string(data: &[RGBW]) -> String {
    data.iter()
        .map(|rgbw| format!("{} {} {} {}", rgbw.r, rgbw.g, rgbw.b, rgbw.w))
        .collect::<Vec<String>>()
        .join(" ")
}

#[tokio::main]
async fn main() -> Result<()> {

    let mut focus = Focus::new_first_available()?;
    let new_palette = string_to_rgbw_vec(COLOR_PALETTE)?;
    focus.palette_rgbw_set(&new_palette).await?;
     
    let the_palette = focus.palette_rgbw_get().await?;

    println!("color: {}", &rgbw_vec_to_string(&the_palette));
    
    Ok(())
}