//$
const COLOR_PALETTE : &str = "6 10 10 100 66 95 112 100 86 114 125 100 130 114 114 100 164 100 124 100 149 147 164 100 151 164 160 100 165 173 174 100 76 91 93 100 66 95 112 100 86 114 125 100 130 114 114 100 164 100 124 100 149 147 164 100 151 164 160 100 165 173 174 100";
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