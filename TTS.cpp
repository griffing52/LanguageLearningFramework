//#include <iostream>
//#include <espeak-ng/speak_lib.h>
//
//void speakIPA(const std::string& ipa) {
//    if (espeak_Initialize(AUDIO_OUTPUT_PLAYBACK, 0, NULL, 0) < 0) {
//        std::cerr << "Failed to initialize eSpeak NG\n";
//        return;
//    }
//
//    espeak_SetVoiceByName("de");  // German voice
//    espeak_Synth(ipa.c_str(), ipa.length() + 1, 0, POS_CHARACTER, 0, espeakCHARS_AUTO, NULL, NULL);
//    espeak_Synchronize();
//}
//
//int main() {
//    std::string ipa = "mir gœnd uf italia vaɪl mir luʃt hend";
//
//    speakIPA(ipa);
//
//    return 0;
//}