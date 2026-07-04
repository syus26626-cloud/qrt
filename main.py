import discord
from discord.ext import commands
import os
import random
import asyncio
import datetime
import string
from keep_alive import keep_alive

# 権限(インテント)の設定
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'ログイン完了: {bot.user.name}')

# ==========================================
# ユーティリティ・便利系コマンド (10個)
# ==========================================
# 1. 応答速度の確認
@bot.command()
async def ping(ctx):
    await ctx.send(f'🏓 Pong! {round(bot.latency * 1000)}ms')

# 2. オウム返し
@bot.command()
async def say(ctx, *, text: str):
    await ctx.message.delete()
    await ctx.send(text)

# 3. 足し算
@bot.command()
async def add(ctx, a: float, b: float):
    await ctx.send(f'計算結果: {a + b}')

# 4. 引き算
@bot.command()
async def sub(ctx, a: float, b: float):
    await ctx.send(f'計算結果: {a - b}')

# 5. 掛け算
@bot.command()
async def mul(ctx, a: float, b: float):
    await ctx.send(f'計算結果: {a * b}')

# 6. 割り算
@bot.command()
async def div(ctx, a: float, b: float):
    if b == 0:
        await ctx.send("0で割ることはできません！")
    else:
        await ctx.send(f'計算結果: {a / b}')

# 7. タイマー機能
@bot.command()
async def timer(ctx, seconds: int):
    await ctx.send(f'⏳ {seconds}秒のタイマーをセットしました！')
    await asyncio.sleep(seconds)
    await ctx.send(f'⏰ {ctx.author.mention} 時間です！')

# 8. 簡易アンケート作成
@bot.command()
async def poll(ctx, *, question: str):
    msg = await ctx.send(f'📊 **アンケート**: {question}')
    await msg.add_reaction('⭕')
    await msg.add_reaction('❌')

# 9. 埋め込みメッセージ作成
@bot.command()
async def embed(ctx, title: str, *, description: str):
    emb = discord.Embed(title=title, description=description, color=discord.Color.green())
    await ctx.send(embed=emb)

# 10. BMI計算
@bot.command()
async def bmi(ctx, height_cm: float, weight_kg: float):
    height_m = height_cm / 100
    res = weight_kg / (height_m ** 2)
    await ctx.send(f'あなたのBMIは **{round(res, 1)}** です。')

# ==========================================
# 情報表示系コマンド (7個)
# ==========================================
# 11. ユーザー情報
@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    emb = discord.Embed(title=f"{member.name} の情報", color=discord.Color.blue())
    emb.add_field(name="ID", value=member.id)
    emb.add_field(name="サーバー参加日", value=member.joined_at.strftime("%Y/%m/%d"))
    await ctx.send(embed=emb)

# 12. サーバー情報
@bot.command()
async def serverinfo(ctx):
    server = ctx.guild
    emb = discord.Embed(title=f"{server.name} の情報", color=discord.Color.orange())
    emb.add_field(name="メンバー数", value=server.member_count)
    emb.add_field(name="作成日", value=server.created_at.strftime("%Y/%m/%d"))
    await ctx.send(embed=emb)

# 13. アイコン画像の拡大表示
@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    emb = discord.Embed(title=f"{member.name} のアイコン")
    emb.set_image(url=member.display_avatar.url)
    await ctx.send(embed=emb)

# 14. Bot自身の情報
@bot.command()
async def botinfo(ctx):
    await ctx.send(f'稼働中のサーバー数: {len(bot.guilds)}\n導入されているコマンド数: {len(bot.commands)}')

# 15. チャンネル情報
@bot.command()
async def channelinfo(ctx):
    await ctx.send(f'チャンネル名: {ctx.channel.name}\nチャンネルID: {ctx.channel.id}')

# 16. 現在時刻の表示
@bot.command()
async def time(ctx):
    now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    await ctx.send(f'現在の時刻: {now}')

# 17. 自分の権限確認
@bot.command()
async def myperms(ctx):
    is_admin = ctx.author.guild_permissions.administrator
    await ctx.send(f'あなたは管理者権限を... {"持っています！" if is_admin else "持っていません。"}')

# ==========================================
# 管理・モデレーション系コマンド (6個)
# ==========================================
# 18. メッセージ一括削除
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f'🧹 {amount}件のメッセージを削除しました。', delete_after=3)

# 19. ユーザーのキック
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'👞 {member.name} をキックしました。')

# 20. ユーザーのBAN
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'🔨 {member.name} をBANしました。')

# 21. チャンネルのロック（書き込み禁止）
@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send('🔒 チャンネルをロックしました。')

# 22. チャンネルのロック解除
@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send('🔓 チャンネルのロックを解除しました。')

# 23. スローモードの設定
@bot.command()
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f'🐌 スローモードを {seconds} 秒に設定しました。')

# ==========================================
# 遊び・ゲーム・ランダム系コマンド (11個)
# ==========================================
# 24. サイコロ
@bot.command()
async def dice(ctx):
    await ctx.send(f'🎲 出目: **{random.randint(1, 6)}**')

# 25. コイントス
@bot.command()
async def coin(ctx):
    result = random.choice(["表 (ウラ)", "裏 (オモテ)"])
    await ctx.send(f'🪙 結果は... **{result}** です！')

# 26. おみくじ
@bot.command()
async def omikuji(ctx):
    luck = random.choice(["大吉", "中吉", "小吉", "吉", "末吉", "凶", "大凶"])
    await ctx.send(f'⛩️ {ctx.author.name} さんの運勢は... **{luck}**！')

# 27. じゃんけん
@bot.command()
async def rps(ctx, hand: str):
    bot_hand = random.choice(["グー", "チョキ", "パー"])
    await ctx.send(f'私は {bot_hand} を出しました！')

# 28. スロットマシン
@bot.command()
async def slot(ctx):
    emojis = ["🍒", "🍇", "🔔", "⭐", "🍉"]
    r1, r2, r3 = random.choice(emojis), random.choice(emojis), random.choice(emojis)
    await ctx.send(f'🎰 [ {r1} | {r2} | {r3} ]')
    if r1 == r2 == r3:
        await ctx.send("🎉 大当たり！")

# 29. 8ボール（魔法の玉に質問）
@bot.command(name="8ball")
async def _8ball(ctx, *, question: str):
    answers = ["確かにそうです。", "間違いなく。", "私の情報源によれば、いいえ。", "今は予測できません。", "非常に疑わしいです。"]
    await ctx.send(f'🎱 答え: {random.choice(answers)}')

# 30. 選択肢からランダムに選ぶ
@bot.command()
async def choose(ctx, *choices: str):
    if not choices:
        await ctx.send("選択肢をスペース区切りで入力してください！")
        return
    await ctx.send(f'🤔 私が選んだのは... **{random.choice(choices)}**')

# 31. 文字列を逆さまにする
@bot.command()
async def reverse(ctx, *, text: str):
    await ctx.send(text[::-1])

# 32. ランダムなパスワード生成
@bot.command()
async def passgen(ctx, length: int = 8):
    chars = string.ascii_letters + string.digits
    password = ''.join(random.choice(chars) for _ in range(length))
    await ctx.author.send(f'🔑 生成されたパスワード: `{password}`\n(安全のためDMで送信しました)')
    await ctx.send('DMにパスワードを送信しました！')

# 33. 指定した範囲のランダムな数字
@bot.command()
async def rand(ctx, min_val: int, max_val: int):
    await ctx.send(f'🔢 結果: {random.randint(min_val, max_val)}')

# 34. LGTM画像の代わり
@bot.command()
async def lgtm(ctx):
    await ctx.send("👍 **L G T M !** (Looks Good To Me!)")


# サーバーの起動とBotの実行
if __name__ == "__main__":
    keep_alive() # Webサーバーを起動
    TOKEN = os.getenv('DISCORD_BOT_TOKEN') # Renderの環境変数から取得
    bot.run(TOKEN)
