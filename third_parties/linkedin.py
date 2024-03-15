import os
import requests

def scrape_linkedin_profile(linkedin_profile_url:str):
    """scrape information from Linkedin profiles,
    manually scrape the information from the Linkedin profile
    """
    # api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
    # header_dic = {"Authorization": f'Bearer 8nP-uaH4i93CVinyvAM5xA'}

    # response = requests.get(
    #     api_endpoint, params={"url": linkedin_profile_url}, headers=header_dic
    # )

    response = requests.get("https://gist.githubusercontent.com/shivamsh314/bd24e781dc087799cdd098f0c0f49c23/raw/598c840379295e5fe17f73fd02e57e793594492d/shivams.json")
    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data
