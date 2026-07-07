// businessOsApi.js - Hat Business OS API routes.
import { getBusinessOsOverview } from './businessOsDb.js';

export function registerBusinessOsRoutes(app, deps) {
  const { safe } = deps;

  app.get('/api/business-os/overview', safe(() => getBusinessOsOverview()));
}
