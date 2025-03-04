//$
const COLOR_PALETTE : &str = "39 38 32 100 198 193 161 100 139 170 156 100 112 130 169 100 181 127 170 100 191 140 177 100 198 152 184 100 201 200 199 100 93 92 87 100 198 193 161 100 139 170 156 100 112 130 169 100 181 127 170 100 191 140 177 100 198 152 184 100 201 200 199 100";
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