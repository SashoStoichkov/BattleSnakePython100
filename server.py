import os, random

import cherrypy
'''
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
'''


class Battlesnake(object):
    def get_bad_positions(self, board):
        bad_positions = []

        for x in range(board['width']):
            bad_positions.append({'x': x, 'y': -1})
            bad_positions.append({'x': x, 'y': (board['height'])})
        for y in range(board['height']):
            bad_positions.append({'x': -1, 'y': y})
            bad_positions.append({'x': (board['width']), 'y': y})

        for snake in board['snakes']:
            for position in snake['body']:
                bad_positions.append(position)

        return bad_positions

    def get_next_moves(self, curr_position):
        return {
            'up': {
                'x': curr_position['x'],
                'y': (curr_position['y'] + 1)
            },
            'down': {
                'x': curr_position['x'],
                'y': (curr_position['y'] - 1)
            },
            'left': {
                'x': (curr_position['x'] - 1),
                'y': curr_position['y']
            },
            'right': {
                'x': (curr_position['x'] + 1),
                'y': curr_position['y']
            },
        }

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        # This function is called when you register your Battlesnake on play.battlesnake.com
        # It controls your Battlesnake appearance and author permissions.
        # TIP: If you open your Battlesnake URL in browser you should see this data
        return {
            'apiversion': '1',
            'author': 'Alexander Stoichov',
            'color': '#ff9225',
            'head': 'gamer',
            'tail': 'mouse',
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        data = cherrypy.request.json

        print('START')
        return 'ok'

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It's how your snake decides where to move.
        # Valid moves are 'up', 'down', 'left', or 'right'.
        # TODO: Use the information in cherrypy.request.json to decide your next move.
        data = cherrypy.request.json

        board = data['board']

        next_moves = self.get_next_moves(data['you']['head'])

        for next_move, position in next_moves.items():
            if position in board['food']:
                return {'move': next_move}

        possible_moves = ['up', 'down', 'left', 'right']
        next_move = random.choice(possible_moves)

        bad_positions = self.get_bad_positions(board)

        print(f'MOVE: {next_move}')
        if next_moves[next_move] not in bad_positions:
            return {'move': next_move}
        else:
            print(next_moves[next_move] in bad_positions)
            return self.move()

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json

        print('END')
        return 'ok'


if __name__ == '__main__':
    server = Battlesnake()
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({
        'server.socket_port':
        int(os.environ.get('PORT', '8080')),
    })
    print('Starting Battlesnake Server...')
    cherrypy.quickstart(server)
