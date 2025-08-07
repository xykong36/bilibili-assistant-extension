#!/usr/bin/env python3
"""
YouTube Video Downloader using yt-dlp

A Python script to download YouTube videos with customizable options.
Compatible with Python 3.12.7 and follows PEP8 coding standards.

Usage:
    python youtube_downloader.py
"""

import os
import sys
import argparse
from typing import Dict, Any, Optional
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    print("Error: yt-dlp is not installed. Please install it using:")
    print("pip install yt-dlp")
    sys.exit(1)


class YouTubeDownloader:
    """A class to handle YouTube video downloads using yt-dlp."""
    
    def __init__(
        self, 
        output_dir: str = "downloads", 
        format_selector: str = "best",
        additional_options: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Initialize the YouTube downloader.
        
        Args:
            output_dir: Directory to save downloaded videos
            format_selector: Video quality format selector
            additional_options: Additional yt-dlp options
        """
        self.output_dir = Path(output_dir)
        self.format_selector = format_selector
        self.additional_options = additional_options or {}
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def download_single_video(self, video_url: str) -> Dict[str, Any]:
        """
        Download a single video from YouTube.
        
        Args:
            video_url: YouTube video URL
            
        Returns:
            Dictionary containing download result information
        """
        if not video_url:
            return {
                'url': video_url,
                'success': False,
                'error': 'No URL provided'
            }
        
        # Set up yt-dlp options
        ydl_opts = {
            'format': self.format_selector,
            'outtmpl': str(self.output_dir / '%(id)s-%(title)s.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
            'ignoreerrors': True,  # Continue on download errors
            'writeinfojson': False,  # Don't write info JSON by default
            'writesubtitles': False,  # Don't download subtitles by default
        }
        
        # Update with any additional options
        ydl_opts.update(self.additional_options)
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract video info first
                info = ydl.extract_info(video_url, download=False)
                
                if not info:
                    return {
                        'url': video_url,
                        'success': False,
                        'error': 'Could not extract video information'
                    }
                
                video_id = info.get('id', 'unknown')
                video_title = info.get('title', 'Unknown Title')
                
                print(f"Downloading: {video_title}")
                print(f"Video ID: {video_id}")
                
                # Download the video
                ydl.download([video_url])
                
                # Prepare filename for return
                filename = ydl.prepare_filename(info)
                
                return {
                    'url': video_url,
                    'video_id': video_id,
                    'title': video_title,
                    'success': True,
                    'filename': filename,
                    'info': {
                        'duration': info.get('duration'),
                        'uploader': info.get('uploader'),
                        'upload_date': info.get('upload_date'),
                        'view_count': info.get('view_count'),
                        'description': info.get('description', '')[:200] + '...'  # Truncate description
                    }
                }
                
        except yt_dlp.DownloadError as e:
            return {
                'url': video_url,
                'success': False,
                'error': f'Download error: {str(e)}'
            }
        except Exception as e:
            return {
                'url': video_url,
                'success': False,
                'error': f'Unexpected error: {str(e)}'
            }
    
    def download_multiple_videos(self, video_urls: list) -> list:
        """
        Download multiple videos from YouTube.
        
        Args:
            video_urls: List of YouTube video URLs
            
        Returns:
            List of dictionaries containing download results
        """
        results = []
        
        for i, url in enumerate(video_urls, 1):
            print(f"\n--- Downloading video {i}/{len(video_urls)} ---")
            result = self.download_single_video(url)
            results.append(result)
            
            if result['success']:
                print(f"✓ Successfully downloaded: {result['title']}")
            else:
                print(f"✗ Failed to download: {result['error']}")
        
        return results
    
    def print_summary(self, results: list) -> None:
        """
        Print a summary of download results.
        
        Args:
            results: List of download result dictionaries
        """
        successful = [r for r in results if r['success']]
        failed = [r for r in results if not r['success']]
        
        print(f"\n{'='*50}")
        print("DOWNLOAD SUMMARY")
        print(f"{'='*50}")
        print(f"Total videos: {len(results)}")
        print(f"Successful: {len(successful)}")
        print(f"Failed: {len(failed)}")
        
        if failed:
            print(f"\nFailed downloads:")
            for result in failed:
                print(f"  • {result['url']}: {result['error']}")


def validate_youtube_url(url: str) -> bool:
    """
    Validate if the URL is a valid YouTube URL.
    
    Args:
        url: URL to validate
        
    Returns:
        True if valid YouTube URL, False otherwise
    """
    youtube_domains = [
        'youtube.com', 'www.youtube.com', 'youtu.be', 
        'm.youtube.com', 'music.youtube.com'
    ]
    
    return any(domain in url.lower() for domain in youtube_domains)


def get_quality_options() -> Dict[str, str]:
    """
    Get available quality format options.
    
    Returns:
        Dictionary of quality options
    """
    return {
        'best': 'best',
        'worst': 'worst',
        'best_video': 'bestvideo+bestaudio/best',
        '1080p': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        '720p': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        '480p': 'bestvideo[height<=480]+bestaudio/best[height<=480]',
        'audio_only': 'bestaudio/best'
    }


def main():
    """Main function to handle command line interface."""
    parser = argparse.ArgumentParser(
        description='Download YouTube videos using yt-dlp',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python youtube_downloader.py -u "https://youtube.com/watch?v=VIDEO_ID"
  python youtube_downloader.py -u "https://youtu.be/VIDEO_ID" -q 720p -o ~/Downloads
  python youtube_downloader.py --urls urls.txt --quality best_video
        """
    )
    
    # URL input options
    url_group = parser.add_mutually_exclusive_group(required=True)
    url_group.add_argument(
        '-u', '--url',
        help='Single YouTube video URL to download'
    )
    url_group.add_argument(
        '--urls',
        help='Text file containing YouTube URLs (one per line)'
    )
    
    # Output options
    parser.add_argument(
        '-o', '--output',
        default='downloads',
        help='Output directory (default: downloads)'
    )
    
    # Quality options
    quality_options = get_quality_options()
    parser.add_argument(
        '-q', '--quality',
        choices=list(quality_options.keys()),
        default='best',
        help=f'Video quality (default: best). Options: {", ".join(quality_options.keys())}'
    )
    
    # Additional options
    parser.add_argument(
        '--audio-only',
        action='store_true',
        help='Download audio only'
    )
    parser.add_argument(
        '--subtitles',
        action='store_true',
        help='Download subtitles'
    )
    parser.add_argument(
        '--info-json',
        action='store_true',
        help='Write video information to JSON file'
    )
    
    args = parser.parse_args()
    
    # Prepare video URLs
    video_urls = []
    
    if args.url:
        if not validate_youtube_url(args.url):
            print("Error: Invalid YouTube URL provided")
            sys.exit(1)
        video_urls = [args.url]
    
    elif args.urls:
        try:
            with open(args.urls, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f if line.strip()]
                
            # Validate URLs
            invalid_urls = [url for url in urls if not validate_youtube_url(url)]
            if invalid_urls:
                print("Error: Invalid YouTube URLs found:")
                for url in invalid_urls:
                    print(f"  {url}")
                sys.exit(1)
            
            video_urls = urls
            
        except FileNotFoundError:
            print(f"Error: File '{args.urls}' not found")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading URLs file: {e}")
            sys.exit(1)
    
    # Set up quality format
    quality_format = quality_options[args.quality]
    if args.audio_only:
        quality_format = 'bestaudio/best'
    
    # Additional options
    additional_options = {}
    if args.subtitles:
        additional_options.update({
            'writesubtitles': True,
            'writeautomaticsub': True,
        })
    if args.info_json:
        additional_options['writeinfojson'] = True
    
    # Create downloader instance
    downloader = YouTubeDownloader(
        output_dir=args.output,
        format_selector=quality_format,
        additional_options=additional_options
    )
    
    print(f"Output directory: {Path(args.output).absolute()}")
    print(f"Quality format: {args.quality}")
    print(f"Number of URLs: {len(video_urls)}")
    
    # Download videos
    if len(video_urls) == 1:
        result = downloader.download_single_video(video_urls[0])
        results = [result]
    else:
        results = downloader.download_multiple_videos(video_urls)
    
    # Print summary
    downloader.print_summary(results)
    
    # Exit with appropriate code
    failed_count = len([r for r in results if not r['success']])
    sys.exit(0 if failed_count == 0 else 1)


if __name__ == "__main__":
    main()
