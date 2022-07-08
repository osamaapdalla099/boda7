from pyrogram import Client, filters
from pyrogram.types import Message

from Music import SUDOERS, app
from Music.MusicUtilities.database.auth import (_get_authusers, delete_authuser, get_authuser,
                            get_authuser_count, get_authuser_names,
                            save_authuser)
from Music.MusicUtilities.helpers.admins import AdminActual
from Music.MusicUtilities.database.changers import (alpha_to_int, int_to_alpha,
                                      time_to_seconds)


@app.on_message(filters.command(["auth", "رفع رتبه", "اد"]) & filters.group)
@AdminActual
async def auth(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                " لرفع رتبه الرد على رسالة المستخدم أو إعطاء اسم المستخدم."
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        user_id = message.from_user.id
        token = await int_to_alpha(user.id)
        from_user_name = message.from_user.first_name
        from_user_id = message.from_user.id
        _check = await get_authuser_names(message.chat.id)
        count = 0
        for smex in _check:
            count += 1
        if int(count) == 20:
            return await message.reply_text(
                "اخرك 20 واحد بس مش ظيطها هي (AUL)"
            )
        if token not in _check:
            assis = {
                "auth_user_id": user.id,
                "auth_name": user.first_name,
                "admin_id": from_user_id,
                "admin_name": from_user_name,
            }
            await save_authuser(message.chat.id, token, assis)
            await message.reply_text(
                f"ابسط يستا اادنلو رول اهو،🥀️."
            )
            return
        else:
            await message.reply_text(f"ايوه يازميلي ده واخد رول.")
        return
    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    user_name = message.reply_to_message.from_user.first_name
    token = await int_to_alpha(user_id)
    from_user_name = message.from_user.first_name
    _check = await get_authuser_names(message.chat.id)
    count = 0
    for smex in _check:
        count += 1
    if int(count) == 20:
        return await message.reply_text(
            "ياعم بالله قولنا ليك 20 واحد بس (AUL)"
        )
    if token not in _check:
        assis = {
            "auth_user_id": user_id,
            "auth_name": user_name,
            "admin_id": from_user_id,
            "admin_name": from_user_name,
        }
        await save_authuser(message.chat.id, token, assis)
        await message.reply_text(
            f"ياله ياعم ابسط ادنلو رول اهو."
        )
        return
    else:
        await message.reply_text(f"ايوه يازميلي ده واخد رول.")


@app.on_message(filters.command(["unauth", "تنزيل رتبه"]) & filters.group)
@AdminActual
async def whitelist_chat_func(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "الرد على رسالة المستخدم أو إعطاء اسم المستخدم او ايدي المستخدم لرفع المستخدم رتبه في البوت"
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        token = await int_to_alpha(user.id)
        deleted = await delete_authuser(message.chat.id, token)
        if deleted:
            return await message.reply_text(
                f"نزلت نا الشخص ده عشان زنان ملوش اي رتبه"
            )
        else:
            return await message.reply_text(f"Not an Authorised User.")
    user_id = message.reply_to_message.from_user.id
    token = await int_to_alpha(user_id)
    deleted = await delete_authuser(message.chat.id, token)
    if deleted:
        return await message.reply_text(
            f"نزلنا الزنان من الرول."
        )
    else:
        return await message.reply_text(f"معلش ياصحبي مينفعش.")


@app.on_message(filters.command("authusers") & filters.group)
async def authusers(_, message: Message):
    _playlist = await get_authuser_names(message.chat.id)
    if not _playlist:
        return await message.reply_text(
            f"No Authorised Users in this Group.\n\nAdd Auth users by /auth and remove by /unauth."
        )
    else:
        j = 0
        m = await message.reply_text(
            "Fetching Authorised Users... Please Wait"
        )
        msg = f"**Authorised Users List[AUL]:**\n\n"
        for note in _playlist:
            _note = await get_authuser(message.chat.id, note)
            user_id = _note["auth_user_id"]
            user_name = _note["auth_name"]
            admin_id = _note["admin_id"]
            admin_name = _note["admin_name"]
            try:
                user = await app.get_users(user_id)
                user = user.first_name
                j += 1
            except Exception:
                continue
            msg += f"{j}➤ {user}[`{user_id}`]\n"
            msg += f"    ┗ Added By:- {admin_name}[`{admin_id}`]\n\n"
        await m.edit_text(msg)
