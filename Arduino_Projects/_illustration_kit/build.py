"""build.py — render every step illustration and copy it where the cards expect it.

Usage:  python build.py 4        # one project
        python build.py 4 5 7    # several
        python build.py all
Outputs <name>.svg into <project>/images/ and <project>/task_cards_he/assets/.
"""
import importlib, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECTS = {
    '4': ('scenes_p4', 'Project_4_Line_Following_Car'),
    '5': ('scenes_p5', 'Project_5_Remote_Controlled_Car'),
    '7': ('scenes_p7', 'Project_7_Camera_Explorer'),
    '8': ('scenes_p8', 'Project_8_Tiny_Quadcopter'),
}


def build(key):
    mod_name, proj = PROJECTS[key]
    sys.path.insert(0, HERE)
    mod = importlib.import_module(mod_name)
    importlib.reload(mod)
    from iso import render
    out_img = os.path.join(HERE, '..', proj, 'images')
    out_ast = os.path.join(HERE, '..', proj, 'task_cards_he', 'assets')
    os.makedirs(out_img, exist_ok=True); os.makedirs(out_ast, exist_ok=True)
    made = []
    for fn in mod.SCENES:
        name, sc, title = fn()
        p = os.path.join(out_img, name + '.svg')
        render(sc, p, title=None)
        shutil.copyfile(p, os.path.join(out_ast, name + '.svg'))
        made.append(name)
        print('  %-38s %s' % (name, title))
    return made


if __name__ == '__main__':
    keys = sys.argv[1:] or ['4']
    if keys == ['all']:
        keys = list(PROJECTS)
    for k in keys:
        print('Project', k)
        build(k)
