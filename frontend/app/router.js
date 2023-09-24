import EmberRouter from '@ember/routing/router';
import config from 'my-app/config/environment';

export default class Router extends EmberRouter {
  location = config.locationType;
  rootURL = config.rootURL;
}

Router.map(function () {
  this.route('student-list', { path: '/' });
  this.route('statistics');
  this.route('statistics-2');
  this.route('statistics-3');
});
