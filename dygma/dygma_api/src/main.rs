//$
const COLOR_PALETTE : &str = "34 22 17 100 175 114 86 100 198 170 150 100 130 159 196 100 100 123 172 100 160 141 160 100 190 182 187 100 199 196 195 100 89 80 76 100 175 114 86 100 198 170 150 100 130 159 196 100 100 123 172 100 160 141 160 100 190 182 187 100 199 196 195 100";
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