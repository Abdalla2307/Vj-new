# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

import re, logging
from pyrogram import Client, filters
from info import DELETE_CHANNELS
from database.ia_filterdb import col, sec_col, unpack_new_file_id

logger = logging.getLogger(__name__)
media_filter = filters.document | filters.video

@Client.on_message(filters.chat(DELETE_CHANNELS) & media_filter)
async def deletemultiplemedia(bot, message):
    """Delete Multiple files from database"""

    for file_type in ("document", "video", "audio"):
        media = getattr(message, file_type, None)
        if media is not None:
            break
    else:
        return

    file_id, file_ref = unpack_new_file_id(media.file_id)

    result = col.delete_one({
        'file_id': file_id,
    })
    if not result.deleted_count:
        result = sec_col.delete_one({
            'file_id': file_id,
        })
    if result.deleted_count:
        logger.info('File is successfully deleted from database.')
    else:
        caption = re.sub(r"(_|\-|\.|\+)", " ", str(media.caption))
        unwanted_chars = ['[', ']', '(', ')']
        for char in unwanted_chars:
            caption = caption.replace(char, '')
        caption = ' '.join(filter(lambda x: not x.startswith('@'), caption.split()))
    
        result = col.delete_many({
            'caption': caption,
            'file_size': media.file_size
        })
        if not result.deleted_count:
            result = sec_col.delete_many({
                'caption': caption,
                'file_size': media.file_size
            })
        if result.deleted_count:
            logger.info('File is successfully deleted from database.')
        else:
            result = col.delete_many({
                'caption': media.caption,
                'file_size': media.file_size
            })
            if not result.deleted_count:
                result = sec_col.delete_many({
                    'caption': media.caption,
                    'file_size': media.file_size
                })
            if result.deleted_count:
                logger.info('File is successfully deleted from database.')
            else:
                logger.info('File not found in database.')
