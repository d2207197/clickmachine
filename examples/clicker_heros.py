
from __future__ import division
from clickmachine import Click, Clicks, Actions, Sleep, Repeat, Move, Coord, CoordsMap

def clicker_heros(left, top, right, bottom):

    coords_map = CoordsMap({
        'next area': Coord(0.8032264379698926, 0.06998040328931704),
        'prev area': Coord(0.6912833969301786, 0.0686068020732221),
        'candy positions': [
            Coord(x=0.4526320850949831, y=0.7132470101280196),
            Coord(x=0.6466923343762987, y=0.6264048887993504),
            Coord(x=0.6598055344710929, y=0.5448068716690171),
            Coord(x=0.7566330192988663, y=0.7538567669700799),
            Coord(x=0.8736523593799909, y=0.6595117305543855),
            Coord(x=0.9141425416527853, y=0.6438832011623719)
        ],
        'attack': Coord(0.7516082388539517, 0.7132103807622571),
        'scroll up': Coord(0.48161988205675976, 0.2959347508897883),
        'scroll down': Coord(0.4817023118111534, 0.9686086335415103),
        'heros skills': Coord(0.17087001171189428, 0.2893414650525326).mxn_points_to(
            Coord(0.36077672439277586, 0.9823266629949208), 7, 5), 
        'heros upgrade/hire': Coord(0.08301363182063286, 0.9558066702075053).n_points_to(
            Coord(0.08318879504871941, 0.2879922834136127), 5),
    }).project_to_space( left = left, top = top,
                         right = right, bottom = bottom)

    
    enable_hero_skills = Actions([ coord.to_click() for coord in coords_map['heros skills']])
    upgrade_heros = Actions([ coord.to_click() for coord in coords_map['heros upgrade/hire']])
    pick_candies = Actions([ coord.to_click() for coord in coords_map['candy positions']])
    
    scroll_up = coords_map['scroll up'].to_click()
    scroll_to_bottom = coords_map['scroll down'].to_clicks(50, 0.01)
    go_next_area = coords_map['next area'].to_move()
    click_next_area = coords_map['next area'].to_click()
    go_prev_area = coords_map['prev area'].to_move()
    click_prev_area = coords_map['prev area'].to_click()

    attack = Repeat(Actions([
        coords_map['attack'].to_clicks(800),
        pick_candies
    ]), times = 3)

    boss_attack = Actions([
        click_next_area,
        go_next_area,
        Sleep(1),
        click_next_area,click_next_area, 
        coords_map['attack'].to_clicks(850),
        Sleep(1),
        go_prev_area,
        Sleep(1),
        click_prev_area,
        Sleep(1),
    ])

    do_upgrades = Actions([
        scroll_to_bottom,
        scroll_up, 
        Repeat(Actions([
            scroll_up,
            enable_hero_skills,
            upgrade_heros,
        ]), times = 5)
    ])

    whole_procesure = Repeat(Actions([
        boss_attack,
        Repeat(Actions([
            attack,
            do_upgrades
        ]), times = 5 )
    ]))

    whole_procesure.act()
    
    
        
if __name__ == '__main__':
    raw_input ('Move the mouse point to TOP-LEFT CORNER of Clicker Heros and press <ENTER>.')
    left, top = Coord.current_coord()
    raw_input ('Move the mouse point to RIGHT-BOTTOM CORNER of Clicker Heros and press <ENTER>.')
    right, bottom = Coord.current_coord()
    clicker_heros(left, top, right, bottom)
