import { config } from '@tamagui/config/v3'
import { createTamagui } from 'tamagui'

const tamaguiConfig = createTamagui({
    ...config,
    themes: {
        ...config.themes,
        light: {
            ...config.themes.light,
            background: '#fff',
            color: '#000',
        },
        dark: {
            ...config.themes.dark,
            background: '#000',
            color: '#fff',
        }
    },
    defaultTheme: 'dark',
    shouldAddPrefersColorThemes: false,
    themeClassNameOnRoot: false,
})

export default tamaguiConfig
export type AppConfig = typeof tamaguiConfig

declare module 'tamagui' {
    // overrides TamaguiCustomConfig so your custom types
    // work everywhere you import `tamagui`
    interface TamaguiCustomConfig extends AppConfig { }
}
