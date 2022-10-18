

first_pass_example = {
  "requests":[
    {
      "image":{
        # "content":"/9j/7QBEUGhvdG9zaG9...image contents...fXNWzvDEeYxxxzj/Coa6Bax//Z"
      },
      "features":[
        {
          "type":"OBJECT_LOCALIZATION",
        #   "maxResults":10
        }
      ]
    }
  ]
}

second_pass_example = {
  "requests":[
    {
      "image":{
        # "content":"/9j/7QBEUGhvdG9zaG9...image contents...fXNWzvDEeYxxxzj/Coa6Bax//Z"
      },
      "features":[
        {
          "type":"IMAGE_PROPERTIES",
        #   "maxResults":10
        }
      ]
    }
  ]
}