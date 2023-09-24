import { module, test } from 'qunit';
import { setupRenderingTest } from 'my-app/tests/helpers';
import { render } from '@ember/test-helpers';
import { hbs } from 'ember-cli-htmlbars';

module('Integration | Component | stastics', function (hooks) {
  setupRenderingTest(hooks);

  test('it renders', async function (assert) {
    // Set any properties with this.set('myProperty', 'value');
    // Handle any actions with this.set('myAction', function(val) { ... });

    await render(hbs`<Stastics />`);

    assert.dom().hasText('');

    // Template block usage:
    await render(hbs`
      <Stastics>
        template block text
      </Stastics>
    `);

    assert.dom().hasText('template block text');
  });
});
