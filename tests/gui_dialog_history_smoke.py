"""Real GUI callbacks and file output; native pickers are replaced with choices."""
import sys
import time
import tempfile
from pathlib import Path
from unittest.mock import patch
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from chrono.gui import App
from chrono.preferences import dialog_directory, read_preferences


def run():
    with tempfile.TemporaryDirectory() as folder:
        root = Path(folder).resolve()
        paths = [root/name for name in ('inputs', 'settings', 'png', 'gif', 'webp', 'bundles')]
        for path in paths: path.mkdir()
        inputs, settings, png, gif, webp, bundles = paths
        Image.new('RGB', (48, 128), 'orange').save(inputs/'test.png')
        with patch('chrono.preferences.preferences_path', return_value=root/'prefs.json'):
            app = App()
            errors = []
            app.report_callback_exception = lambda *args: errors.append(str(args))
            def wait():
                start = time.monotonic()
                while app.busy or app.after_preview or app.result is None:
                    app.update(); time.sleep(.02)
                    assert time.monotonic()-start < 90, app.status.get()
                app.update()
            def choose(method, callback, selection, expected):
                with patch('chrono.gui.filedialog.'+method, return_value=str(selection)) as picker:
                    callback()
                    assert Path(picker.call_args.kwargs['initialdir']) == expected, picker.call_args
            try:
                wait()
                choose('askopenfilename', app.open_image, inputs/'test.png', Path.home()); wait()
                choose('asksaveasfilename', app.save_settings, settings/'test.json', Path.home())
                choose('asksaveasfilename', app.save_preview, png/'test.png', settings)
                choose('asksaveasfilename', app.save_gif, gif/'test.gif', png)
                app.export_animated_preview(); app.update()
                choose('asksaveasfilename', app.animation_export_dialog.save, webp/'test.webp', gif)
                choose('askdirectory', app.export, bundles, webp)
                assert dialog_directory('save')['initialdir'] == str(bundles)
                assert len(list(bundles.glob('*/image.bin'))) == 1
                choose('askopenfilename', app.load_settings, settings/'test.json', inputs); wait()
                choose('askopenfilename', app.open_image, inputs/'test.png', settings); wait()
                for path in (settings/'test.json', png/'test.png', gif/'test.gif', webp/'test.webp'):
                    assert path.stat().st_size > 0, path
                previous = read_preferences()
                for method, callback in [('askopenfilename', app.open_image), ('askopenfilename', app.load_settings),
                                         ('asksaveasfilename', app.save_settings), ('asksaveasfilename', app.save_preview),
                                         ('asksaveasfilename', app.save_gif), ('askdirectory', app.export)]:
                    with patch('chrono.gui.filedialog.'+method, return_value=''):
                        callback()
                    assert read_preferences() == previous
                app.export_animated_preview(); app.update()
                choose('asksaveasfilename', app.animation_export_dialog.save, '', bundles)
                assert read_preferences() == previous
                app.animation_export_dialog.destroy()
                with patch('chrono.gui.messagebox.showerror'):
                    choose('askopenfilename', app.open_image, root/'missing.png', inputs)
                    choose('askopenfilename', app.load_settings, root/'missing.json', inputs)
                    with patch.object(app, 'export_to', side_effect=OSError('failed')):
                        choose('askdirectory', app.export, root, bundles)
                    with patch('chrono.core.Settings.save', side_effect=OSError('failed')):
                        choose('asksaveasfilename', app.save_settings, root/'failed.json', bundles)
                    app.export_animated_preview(); app.update()
                    with patch('chrono.web_preview.export_animation', side_effect=OSError('failed')):
                        choose('asksaveasfilename', app.animation_export_dialog.save, root/'failed.webp', bundles)
                    app.animation_export_dialog.destroy()
                assert read_preferences() == previous
                assert not errors, errors
                print('Dialog GUI passed: separate open/save defaults, settings, PNG, GIF, WebP, bundle parent, cancellation and failures.')
            finally:
                app.close()


if __name__ == '__main__': run()
