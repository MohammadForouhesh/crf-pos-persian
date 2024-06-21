"""
Run the Application

....................................................................................................
MIT License

Copyright (c) 2021-2023 AUT Iran, Mohammad H Forouhesh
Copyright (c) 2021-2022 MetoData.ai, Mohammad H Forouhesh
....................................................................................................
This module serves as unit testing for various functionalities in the code.
"""

import logging 
from app import create_app
from flask import request

from crf_pos.pos_tagger.meta_tagger import MetaTagger
from crf_pos.pos_tagger.wapiti import WapitiPosTagger

app = create_app()
tagger: MetaTagger = WapitiPosTagger()


@app.route('/infering', methods=['POST'])
def infering():
    post_data = request.get_json(force=True)
    return tagger[post_data['stdin']]


if __name__ == '__main__':
    logging.basicConfig(filename="std.log", 
                        format='%(asctime)s %(message)s', 
                        filemode='w') 
    logger=logging.getLogger() 

    logger.setLevel(logging.WARNING) 
    app.run()