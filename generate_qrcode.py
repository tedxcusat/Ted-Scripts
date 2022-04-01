import qrcode
import json

users = json.loads(open("data/users.json").read())
failed = []
count = 1

for user in users:
    try:
        data = f"https://admin-tedx.vercel.app/search?email={user['email']}"
        # # Encoding data using make() function
        img = qrcode.make(data)

        # # Saving as an image file
        img.save(f"qrcodes/{user['email'].split('@')[0]}.png")
        print(f"{count}: Success: {user['email']} - QRCode generation")
    except Exception as e:
        print(f"{count}: Failure: {user['email']} - QRCode generation")
        failed.append(user["email"])
    count += 1
