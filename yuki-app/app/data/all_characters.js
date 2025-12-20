// Parsing logic helper 
const parseFilename = (path) => {
    // Extract filename from path
    const filename = path.split('/').pop();

    // Default fallback
    let name = "Unknown";
    let series = "Cosplay";

    // Pattern: [subject]_as_[character]_from_[series]
    // Example: v12_5_drake_as_daffy_duck_from_looney_tunes...
    const asIndex = filename.indexOf('_as_');
    const fromIndex = filename.indexOf('_from_');

    if (asIndex !== -1) {
        // Extract Character Name
        // Start after '_as_'
        let charStart = asIndex + 4;
        let charEnd = fromIndex !== -1 ? fromIndex : filename.lastIndexOf('_'); // fallback to last underscore if 'from' missing, or just end

        // If no 'from', try to find where the suffix tags start
        if (fromIndex === -1) {
            const doubleUnder = filename.indexOf('__', charStart);
            if (doubleUnder !== -1) charEnd = doubleUnder;
        }

        let rawName = filename.substring(charStart, charEnd).replace(/_/g, ' ');
        // Proper Case
        name = rawName.replace(/\b\w/g, c => c.toUpperCase());
    } else {
        // Fallback for files without _as_ (e.g. top15_01_Luffy_4k.png)
        // Try to parse typical naming conventionally
        const parts = filename.split('_');
        if (parts.length > 2) {
            // Check for known patterns or just take the middle chunk
            // e.g. top15_01_Luffy_4k -> Luffy
            // e.g. Snow_New_Now_Glasses_John_Wick_v9 -> John Wick
            const vIndex = parts.findIndex(p => p.startsWith('v9') || p.startsWith('v12') || p === '4k');
            if (vIndex !== -1) {
                name = parts.slice(0, vIndex).join(' ').replace(/top15 \d+ /, '').trim();
            } else {
                name = parts.slice(2, parts.length - 1).join(' '); // very rough guess
            }
            name = name.replace(/\b\w/g, c => c.toUpperCase());
        }
    }

    if (fromIndex !== -1) {
        // Extract Series
        let seriesStart = fromIndex + 6;
        let seriesEnd = filename.indexOf('__', seriesStart);
        if (seriesEnd === -1) seriesEnd = filename.lastIndexOf('_'); // fallback

        let rawSeries = filename.substring(seriesStart, seriesEnd).replace(/_/g, ' ');
        series = rawSeries.replace(/\b\w/g, c => c.toUpperCase());
    }

    // Heuristic Cleanups
    name = name.replace("Purple Brand Model", "Model").replace("Paris Hilton", "Paris");
    name = name.replace(/_/g, " ").trim();
    if (name.includes("Nini As")) name = name.replace("Nini As", "").trim();

    // Convert local C:/ path to localhost server URL
    // Root of server is C:\Yuki_Local\Cosplay_Lab\Renders
    // We need to match the relative path from there.
    // Example Input: C:/Yuki_Local/Cosplay_Lab/Renders/Renders_Nini_Black_Waifu/file.png
    // Output: http://localhost:8083/Renders_Nini_Black_Waifu/file.png

    const serverRoot = "http://127.0.0.1:8083/";
    const localPrefix = "C:/Yuki_Local/Cosplay_Lab/Renders/";

    // Normalize path to forward slashes just in case
    let normalizedPath = path.replace(/\\/g, '/');
    let uri = normalizedPath;

    if (normalizedPath.startsWith(localPrefix)) {
        uri = serverRoot + normalizedPath.replace(localPrefix, '');
    }

    return { name, series, uri };
};

export const FULL_CHARACTER_POOL = [
    { id: 1, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/Renders_Nini_Black_Waifu/v12_5_nini_as_ghislaine_dedoldia_from_mushoku_tensei__live_action_cosplay__hyper_realistic___dark_skin__voluptuous_body__curvy__thick_thighs__fitness_model_physique__toned_abs__cleavage__8k_131014.png") },
    { id: 2, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/Renders_Nini_Black_Waifu/v12_5_nini_as_hibana_from_fire_force__live_action_cosplay__hyper_realistic___dark_skin__voluptuous_body__curvy__thick_thighs__fitness_model_physique__toned_abs__cleavage__8k_130912.png") },
    { id: 3, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/Renders_Nini_Black_Waifu/v12_5_nini_as_yoruichi_shihouin_from_bleach__live_action_cosplay__hyper_realistic___dark_skin__voluptuous_body__curvy__thick_thighs__fitness_model_physique__toned_abs__cleavage__8k_130802.png") },
    { id: 4, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/Renders_Purple_Bikini_Batch/v12_5_purple_brand_model_as_yor_forger_from_spy_x_family__live_action_cosplay__hyper_realistic___wearing_bikini__swimsuit__summer_vibes__beach_background__cleavage__tanned_skin__8k_125429.png") },
    { id: 5, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/Renders_Purple_Bikini_Batch/v12_5_purple_brand_model_as_asuna_yuuki_from_sword_art_online__live_action_cosplay__hyper_realistic___wearing_bikini__swimsuit__summer_vibes__beach_background__cleavage__tanned_skin__8k_125346.png") },
    { id: 6, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/Renders_Purple_Bikini_Batch/v12_5_purple_brand_model_as_nami_from_one_piece__live_action_cosplay__hyper_realistic___wearing_bikini__swimsuit__summer_vibes__beach_background__cleavage__tanned_skin__8k_124448.png") },
    { id: 7, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/Renders_Purple_Bikini_Batch/v12_5_purple_brand_model_as_nami_from_one_piece__live_action_cosplay__hyper_realistic___wearing_bikini__swimsuit__summer_vibes__beach_background__cleavage__tanned_skin__8k_124020.png") },
    { id: 8, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/Renders_Purple_Winter_Batch/v12_5_purple_brand_model_as_frieren_from_frieren__live_action_cosplay__hyper_realistic___wearing_winter_outfit__heavy_fur_coat__scarf__snow_background__cold_breath__cinematic_lighting_123449.png") },
    { id: 9, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/Renders_Purple_Winter_Batch/v12_5_purple_brand_model_as_emilia_from_re_zero__live_action_cosplay__hyper_realistic___wearing_winter_outfit__heavy_fur_coat__scarf__snow_background__cold_breath__cinematic_lighting_123407.png") },
    { id: 10, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/Renders_Drake_Combined/v12_5_drake_as_daffy_duck_from_looney_tunes__live_action_cosplay__hyper_realistic__105708.png") },
    { id: 11, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/Renders_Drake_Combined/v12_5_drake_as_shinji_ikari_from_evangelion__live_action_cosplay__hyper_realistic__105448.png") },
    { id: 12, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/Renders_Drake_Combined/v12_5_drake_as_takemichi_hanagaki_from_tokyo_revengers__live_action_cosplay__hyper_realistic__105434.png") },
    { id: 13, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/Renders_Drake_Combined/v12_5_drake_as_subaru_natsuki_from_re_zero__live_action_cosplay__hyper_realistic__105415.png") },
    { id: 14, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/Renders_Halle_V12_5/v12_5_halle_berry_as_sakiko_togawa_from_bang_dream__ave_mujica_101959.png") },
    { id: 15, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/Renders_Halle_V12_5/v12_5_halle_berry_as_chinatsu_kano_from_blue_box_101908.png") },
    { id: 16, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/Renders_Halle_V12_5/v12_5_halle_berry_as_emilia_from_re_zero_101831.png") },
    { id: 17, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/Renders_Halle_V12_5/v12_5_halle_berry_as_hina_chono_from_blue_box_101807.png") },
    { id: 18, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/Renders_Halle_V12_5/v12_5_halle_berry_as_maomao_from_the_apothecary_diaries_101736.png") },
    { id: 19, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/Renders_Paris_Single_V12/v12_paris_hilton_as_makima_093700.png") },
    { id: 20, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/Renders_Paris_Single_V12/v12_paris_hilton_as_boa,_hancock_093723.png") },
    { id: 21, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/Renders_Paris_Single_V12/v12_paris_hilton_as_kitagawa,_marin_093752.png") },
    { id: 22, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/Renders_Paris_Single_V12/v12_paris_hilton_as_zero_two_094140.png") },
    { id: 23, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/Renders_V12_Weird/v12_elon_musk_as_ryuk_(death_note)_084657.png") },
    { id: 24, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/Renders_V12_Weird/v12_elon_musk_as_orochimaru_(naruto)_084850.png") },
    { id: 25, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/Renders_V12_Weird/v12_elon_musk_as_no-face_(spirited_away)_085109.png") },
    { id: 26, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/kai_bella_v10/kai_bella_04_HD-wallpaper-bella-forest-movi.png") },
    { id: 27, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/v9_results/Jordan_new_test/Good/Jordan_new_test_Starfire_v9_2pass_gen1_053113.png") },
    { id: 28, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/v9_results/Jordan_new_test/Good/Jordan_new_test_Wonder_Woman_v9_2pass_gen1_052728.png") },
    { id: 29, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/v9_results/Jordan_new_test/Good/Jordan_new_test_Sailor_Moon_v9_low_gen1_050717.png") },
    { id: 30, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/v9_results/Jordan_new_test/Good/Jordan_new_test_Nezuko_Kamado_v9_low_gen1_050644.png") },
    { id: 31, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/v9_results/Snow New Now Glasses/Snow New Now Glasses_Captain_America_v9_gen1_215336.png") },
    { id: 32, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/v9_results/Snow New Now Glasses/Snow New Now Glasses_Thor_v9_gen1_215256.png") },
    { id: 33, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/v9_results/Snow New Now Glasses/Snow New Now Glasses_Wonder_Woman_v9_gen1_214535.png") },
    { id: 34, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/v9_results/Snow New Now Glasses/Snow New Now Glasses_Black_Widow_v9_gen1_214419.png") },
    { id: 35, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/v9_results/Snow New Now Glasses/Snow New Now Glasses_Neo_v9_gen1_213424.png") },
    { id: 36, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/v9_results/Snow New Now Glasses/Snow New Now Glasses_Geralt_of_Rivia_v9_gen1_193923.png") },
    { id: 37, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/v9_results/Snow New Now Glasses/Snow New Now Glasses_Black_Panther_v9_gen1_193746.png") },
    { id: 38, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/v9_results/Snow New Now Glasses/Snow New Now Glasses_John_Wick_v9_gen1_193423.png") },
    { id: 39, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/snow_v4_advanced_results/V4_Tifa_Lockhart_Anime_20251208_145539.png") },
    { id: 40, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/unified_test_results/02_Top15_Batch/top15_01_Luffy_4k.png") },
    { id: 41, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/unified_test_results/02_Top15_Batch/top15_02_Gojo_Satoru_4k.png") },
    { id: 42, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/unified_test_results/02_Top15_Batch/top15_03_Tanjiro_Kamado_4k.png") },
    { id: 43, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/unified_test_results/02_Top15_Batch/top15_04_Naruto_Uzumaki_4k.png") },
    { id: 44, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/unified_test_results/02_Top15_Batch/top15_05_Spike_Spiegel_4k.png") },
    { id: 45, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/unified_test_results/02_Top15_Batch/top15_06_Edward_Elric_4k.png") },
    { id: 46, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/unified_test_results/02_Top15_Batch/top15_07_Goku_4k.png") },
    { id: 47, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/unified_test_results/02_Top15_Batch/top15_08_Levi_Ackerman_4k.png") },
    { id: 48, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/unified_test_results/02_Top15_Batch/top15_09_Saitama_4k.png") },
    { id: 49, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/unified_test_results/02_Top15_Batch/top15_10_Ichigo_Kurosaki_4k.png") },
    { id: 50, ...parseFilename("C:/Yuki_Local/Cosplay_Lab/Renders/unified_test_results/02_Top15_Batch/top15_11_Eren_Yeager_4k.png") },
];
