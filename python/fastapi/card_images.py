# Serve the card image along with the card data
card_image_path = card_images_dir / f"{card['value']}_{card['suit']}.jpg"
if card_image_path.is_file():
    return {
        "card": card,
        "image_path": card_image_path
    }
else:
    raise HTTPException(status_code=500, detail=f"Image not found for card {card_key}.")

# New endpoint to serve card images
@app.get("/card_image/{image_name}")
def get_card_image(image_name: str):
    image_path = card_images_dir / image_name
    if image_path.is_file():
        return FileResponse(image_path)
    else:
        raise HTTPException(status_code=404, detail=f"Image {image_name} not found.")
