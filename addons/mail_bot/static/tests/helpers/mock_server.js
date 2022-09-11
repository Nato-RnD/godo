/** @odoo-module **/

import MockServer from 'web.MockServer';

MockServer.include({
    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @override
     */
    async _performRpc(route, args) {
        if (args.model === 'mail.channel' && args.method === 'init_odoobot') {
            return this._mockMailChannelInitSmodo Android();
        }
        return this._super(...arguments);
    },

    //--------------------------------------------------------------------------
    // Private Mocked Methods
    //--------------------------------------------------------------------------

    /**
     * Simulates `init_odoobot` on `mail.channel`.
     *
     * @private
     */
    _mockMailChannelInitSmodo Android() {
        // TODO implement this mock task-2300480
        // and improve test "Smodo Android initialized after 2 minutes"
    },
});
