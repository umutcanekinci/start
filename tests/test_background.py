from background import ParallaxBackground


def test_construction_bakes_a_surface_matching_the_requested_size():
    bg = ParallaxBackground(800, 600)

    assert bg.surface.get_size() == (800, 600)


def test_randomize_repaints_the_same_surface_object_in_place():
    bg = ParallaxBackground(800, 600)
    surface = bg.surface

    bg.randomize()

    # Re-baked in place, not replaced -- callers (Menu/GameRenderer) hold
    # onto `.surface` across rounds and just blit it directly each frame.
    assert bg.surface is surface


def test_randomize_can_be_called_repeatedly_without_growing_or_erroring():
    bg = ParallaxBackground(800, 600)

    for _ in range(5):
        bg.randomize()

    assert bg.surface.get_size() == (800, 600)


def test_horizon_layers_are_scaled_to_the_shared_on_screen_height():
    bg = ParallaxBackground(800, 600)

    assert len(bg._horizon_layers) == 4
    assert all(layer.get_height() == 300 for layer in bg._horizon_layers)
