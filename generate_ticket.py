import json
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

users = json.loads(open("data/users.json").read())
failed = []
count = 1

start = 1190
end = 1650

font_name = ImageFont.truetype("data/Poppins-Regular.ttf", 36)
font_email = ImageFont.truetype("data/Poppins-Regular.ttf", 20)

for user in users:
    img = Image.open("data/ticket_template.png")
    try:
        qr = Image.open(f"qrcodes/{user['email'].split('@')[0]}.png").resize((200, 200))
        I1 = ImageDraw.Draw(img)

        text_start = 396
        img.paste(qr, (start + 130, 130), mask=qr)
        I1.text(
            (start + (end - start) / 2 - 22 * len(user["name"]) / 2, 396),
            user["name"],
            font=font_name,
            fill=(255, 255, 255),
        )
        I1.text(
            (start + (end - start) / 2 - 12.5 * len(user["email"]) / 2, 446),
            user["email"],
            font=font_email,
            fill=(255, 255, 255),
        )
        I1.text(
            (start + (end - start) / 2 - 12.5 * len(user["phno"]) / 2, 486),
            user["phno"],
            font=font_email,
            fill=(255, 255, 255),
        )
        I1.text((580, 513), str(user["seatNo"]), font=font_email, fill=(255, 255, 255))

        # img.show()

        img.save(f"tickets/{user['email'].split('@')[0]}.png")
        print(f"{count}: Success: {user['email']} - Ticket generation")
    except Exception as e:
        print(f"{count}: Failure: {user['email']} - Ticket generation")
        failed.append(user["email"])
    count += 1
