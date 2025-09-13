import sqlite3

# Group ID را اینجا قرار دهید (مثلاً -1001234567890)
# ابتدا group ID را پیدا کنید و اینجا قرار دهید
group_id = -1003064107237  # Group ID واقعی

conn = sqlite3.connect('feedback_bot.db')
cursor = conn.cursor()
cursor.execute('UPDATE bots SET "group" = ? WHERE id = 1', (group_id,))
conn.commit()
print(f'Bot group updated to: {group_id}')
conn.close()
