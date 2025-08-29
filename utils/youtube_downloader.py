import yt_dlp
import ffmpeg
import os


def yt_downloader(url, format="best", path="Queue_Download/%(title)s.%(ext)s", volume=0.0, bass=0.0, audio_bitrate=500000):
    # Create a yt-dlp downloader object with custom options

    filenames = {}

    if format == "mp3":
        ydl_opts = {
        'outtmpl': path,
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
            }],
        }
    else:
        ydl_opts = {
        'outtmpl': path,
        'format': format
        }
    #try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        ydl.download([url])

        try:

            for video_info in info['entries']:
                video_title = video_info.get('title', 'Unknown')
                filename = ydl.prepare_filename(video_info)

                adjusted_filename = f"{filename.split('.')[0]}_adjusted.{filename.split('.')[1]}"
                ffmpeg.input(filename).output(adjusted_filename, af=f"volume={volume}, bass=g={bass}", ab=audio_bitrate).run(overwrite_output=True)
                os.remove(filename)
                filename = adjusted_filename


                filenames[filename] = video_title
        except:

            filename = ydl.prepare_filename(info)

            adjusted_filename = f"{filename.split('.')[0]}_adjusted.{filename.split('.')[1]}"
            ffmpeg.input(filename).output(adjusted_filename, af=f"volume={volume}, bass=g={bass}").run(overwrite_output=True)
            os.remove(filename)
            filenames[adjusted_filename] = info.get("title", "unknown")

    return filenames


if __name__ == "__main__":
    video_url = input("Paste YT link here:")
    format = input("format (mp3, best, bestaudio):")
    yt_downloader(video_url, format=format)
    # filename = yt_downloader(video_url, format="bestaudio")
    # print(filename)
    # yt_downloader(video_url, format=format)



