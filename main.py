"""
Name: Bandcamp song downloader
Author: thatjamesemo
Ver: 1.0.1 (ALPHA)
"""

# TODO: Add a UI to the project, or a website on the Github page to save these to.

import urllib.request
import requests


def create_dictionary(links):
    """
    Creates a dictionary from separating the link titles from the links themselves.
    :param links: list
    :return: dict, list
    """
    return_dict = {}
    return_list = []

    for item in links:
        count = 1
        while item[-count] != "/":
            count += 1
        count -= 1
        return_dict[item[-count:]] = item
        return_list.append(item[-count:])

    return return_dict, return_list


def get_html(website):
    """
    Returns the HTML content of a website as a string.
    :param website: string
    :return: string
    """
    response = urllib.request.urlopen(website)
    html_content = response.read().decode('utf-8')

    return html_content


def get_image(html_contents):
    """
    Gets the bytes for the image file.
    :param html_contents:
    :return: bytes
    """

    popup_images = []
    for element in html_contents:
        if "<a class=\"popupImage\"" in element:
            popup_images.append(element)
    image_link = popup_images[0].replace("<a class=\"popupImage\" href=\"", "").replace("\">", "").replace(" ", "")

    return requests.get(image_link).content


def get_song_file(html_contents):
    """
    Gets the binary for the mp3 files.
    :param html_contents:
    :return: list
    """

    links = []
    content = []
    for element in html_contents:
        if "https://t4.bcbits.com" in element:
            temp_list = element.split("https://")
            for item in temp_list:
                if "t4.bcbits.com" in item:
                    links.append("https://" + item.replace("}", ""))

    for link in links:
        content.append(requests.get(link).content)

    return content


def get_files(dict_links, names_of_songs, save_folder):
    """
    Gets the files for the
    :param dict_links: dict
    :param names_of_songs: list
    :param save_folder: string
    :return: null
    """

    # TODO: Split up the creation of files into seperate commands, to save space and simplicity.
    # TODO: Add in support for album accounts.

    for name in names_of_songs:
        song_name = name
        song_link = dict_links.get(song_name)

        html_contents = get_html(song_link).split("\n")

        image_content = get_image(html_contents)
        with open(f"{save_folder}/{song_name}.jpg", "wb") as file:
            file.write(image_content)
            print("Image " + f"{save_folder}/{song_name}.jpg" + " has been saved.")
            file.close()

        song_bytes = get_song_file(html_contents)
        for binary in song_bytes:
            with open(f"{save_folder}/{song_name}.mp3", "wb") as file:
                file.write(binary)
                print("Song " + f"{save_folder}/{song_name}.mp3 has been saved. \n")
                file.close()


def main():
    location = input("Please enter the location of the .TXT file with the links you want to download the song for: ")
    save_folder = input("Please enter the location of the folder where you want to save this content: ")
    with open(location, 'r') as file:
        links = file.readlines()
        for item in links:
            links[links.index(item)] = item.replace("\n", "")
        n_links = []
        for link in links:
            if "/album/" not in link:
                n_links.append(link)
        file.close()
    dict_links, names_of_songs = create_dictionary(n_links)

    get_files(dict_links, names_of_songs, save_folder)


if __name__ == "__main__":
    main()
