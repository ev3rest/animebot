from aiogram import types
from enums import Functions
def normalkeyboard(command_id, post_id):
	keyboard = types.InlineKeyboardMarkup(row_width=1)
	row_btns = (types.InlineKeyboardButton('Download', callback_data='%s:%s'%(Functions.DOWNLOAD, post_id)),\
				types.InlineKeyboardButton('Next', callback_data='%s:%s' %(Functions.NEXT, command_id))) #function:data
	keyboard.row(*row_btns)
	return keyboard