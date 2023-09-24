import { module, test } from 'qunit';
import { setupRenderingTest } from 'my-app/tests/helpers';
import { render } from '@ember/test-helpers';
import { hbs } from 'ember-cli-htmlbars';

module('Integration | Component | statistics-3', function (hooks) {
  setupRenderingTest(hooks);

  test('it renders', async function (assert) {
    // Set any properties with this.set('myProperty', 'value');
    // Handle any actions with this.set('myAction', function(val) { ... });

    await render(hbs`<Statistics3 />`);

    assert.dom().hasText('');

    // Template block usage:
    await render(hbs`
      <Statistics3>
        template block text
      </Statistics3>
    `);

    assert.dom().hasText('template block text');
  });
});
