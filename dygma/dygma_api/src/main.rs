//$
const COLOR_PALETTE : &str = "33 20 16 100 170 104 84 100 171 83 35 100 171 128 59 100 198 145 29 100 176 167 89 100 134 159 162 100 199 196 195 100 88 78 75 100 170 104 84 100 171 83 35 100 171 128 59 100 198 145 29 100 176 167 89 100 134 159 162 100 199 196 195 100";
//&

use dygma_focus::prelude::*;
use anyhow::{bail, Result};

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

#[tokio::main]
async fn main() -> Result<()> {

    let mut focus = Focus::new_first_available()?;
    let new_palette = string_to_rgbw_vec(COLOR_PALETTE)?;
    focus.palette_rgbw_set(&new_palette).await?;
     
    Ok(())
}