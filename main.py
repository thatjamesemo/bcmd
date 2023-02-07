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


def get_files(dict_links, names_of_songs, save_folder):
    """
    Gets the files for the
    :param dict_links: dict
    :param names_of_songs: list
    :param save_folder: string
    :return:
    """

    for name in names_of_songs:
        song_name = name
        song_link = dict_links.get(song_name)

        html_contents = get_html(song_link).split("\n")
        popup_images = []
        for element in html_contents:
            if "<a class=\"popupImage\"" in element:
                popup_images.append(element)
        image_link = popup_images[0].replace("<a class=\"popupImage\" href=\"", "").replace("\">", "").replace(" ", "")
        print("Image " + f"{save_folder}/{song_name}.jpg" + " has been saved")

        with open(f"{save_folder}/{song_name}.jpg", "wb") as file:
            file.write(requests.get(image_link).content)
            file.close()
        # TODO: Trigger the button to download the music on these pages.

        links = []
        for element in html_contents:
            if "<script" in element and "mp3-128" in element:
                links.append(element)
                print(element)

        print("\n\n")




def main():
    location = input("Please enter the location of the .TXT file with the links you want to download the song for: ")
    save_folder = input("Please enter the location of the folder where you want to save this content: ")
    with open(location, 'r') as file:
        links = file.readlines()
        for item in links:
            links[links.index(item)] = item.replace("\n", "")
        n_links = []
        for link in links:
            if not "/album/" in link:
                n_links.append(link)
        file.close()
    dict_links, names_of_songs = create_dictionary(n_links)

    get_files(dict_links, names_of_songs, save_folder)


if __name__ == "__main__":
    main()
