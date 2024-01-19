//$
const COLOR_PALETTE : &str = "220 10 19 100 176 16 13 100 128 69 91 100 235 99 37 100 146 125 180 100 87 166 212 100 204 140 119 100 169 174 191 100 83 94 127 100 176 16 13 100 128 69 91 100 235 99 37 100 146 125 180 100 87 166 212 100 204 140 119 100 169 174 191 100";
//&

use anyhow::Result;
use anyhow::bail;
use dygma_focus::prelude::*;

pub(crate) fn rgbw_vec_to_string(data: &[RGBW]) -> String {
    data.iter()
        .map(|rgbw| format!("{} {} {} {}", rgbw.r, rgbw.g, rgbw.b, rgbw.w))
        .collect::<Vec<String>>()
        .join(" ")
}

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
    // Open the first device found and declare as mutable
    // Other constructors are under Focus::new_*

    let mut focus = Focus::new_first_available()?;
    let new_palette = string_to_rgbw_vec(COLOR_PALETTE)?;
    focus.palette_rgbw_set(&new_palette).await?;
    println!("color: {}", &rgbw_vec_to_string(&new_palette));

    

    //let palette = &focus.palette_rgb_get()?;
    //focus.string
    // for color in palette{
    //     println!("color: {}", &color);
    // }
    //0 0 0 0 0 254 24 0 0 0 0 255 231 255 0 0 0 254 234 0 0 52 255 0 206 0 25 2 0 77 168 87 125 0 235 19 20 0 36 219 85 0 126 129 210 131 0 35 143 82 0 100 97 91 0 144 44 72 0 115 142 49 0 94

    //255 255 255 255 255 254 24 255 255 255 255 255 231 255 255 255 255 254 234 255 255 52 255 255 206 255 25 2 255 77 168 87 125 255 235 19 20 255 36 219 85 255 126 129 210 131 255 35 143 82 255 100 97 91 255 144 44 72 255 115 142 49 255 94

    //focus.palette_set(COLOR_PALETTE)?;
    //focus.palette_rgbw_set("220 95 112 140 254 24 0 0 0 0 255 231 255 0 0 0 254 234 0 0 52 255 0 206 0 25 2 0 77 168 87 125 0 235 19 20 0 36 219 85 0 126 129 210 131 0 35 143 82 0 100 97 91 0 144 44 72 0 115 142 49 0 94").await?;
    //println!("palette: {}", &focus.palette_get()?);
    Ok(())
}

//const color_3 : &str = "rgba(86,114,125,1.0)";
//const color_2 : &str = "rgba(66,95,112,1.0)";
//const color_1 : &str = "rgba(6,10,10,1.0)";