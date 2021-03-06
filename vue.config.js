module.exports = {
    pluginOptions: {
        electronBuilder: {
            externals: [
                'electron-log'
            ],
            nodeIntegration: false,
            preload: 'src/preload.js',
            builderOptions: {
                appId: 'com.megasanjay.electronvueflask',
                afterSign: './scripts/notarize.js',
                asar: true,
                generateUpdatesFilesForAllChannels: true,
                files: [
                    '**/*',
                    '!pyflask/',
                    '!build/',
                    '!api.spec'
                ],
                win: {
                    target: 'nsis',
                    icon: './src/assets/app-icons/windowsAppIcon.ico',
                    extraResources: [{
                        from: './src/pyflaskdist/api.exe'
                    }]
                },
                mac: {
                    target: [
                        'dmg',
                        'zip'
                    ],
                    icon: './src/assets/app-icons/macAppIcon.png',
                    extraResources: [{
                        from: './src/pyflaskdist/api'
                    }],
                    darkModeSupport: false,
                    hardenedRuntime: true,
                    gatekeeperAssess: false,
                    entitlements: './entitlements.mac.inherit.plist',
                    entitlementsInherit: './entitlements.mac.inherit.plist'
                },
                linux: {
                    target: 'AppImage',
                    icon: './src/assets/app-icons/linuxAppIcon.png',
                    extraResources: [{
                        from: './src/pyflaskdist/api'
                    }]
                },
                nsis: {
                    createDesktopShortcut: 'always',
                    oneClick: true,
                    deleteAppDataOnUninstall: true,
                    installerIcon: './src/assets/app-icons/windowsAppIcon.ico'
                },
            }
        },
        vuetify: {
            // https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vuetify-loader
        }
    },
};
