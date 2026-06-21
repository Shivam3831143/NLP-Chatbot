from deep_translator import GoogleTranslator

# Test translating Hindi to English
hindi_text = "मुझे बहुत तेज़ बुखार है"
english_translation = GoogleTranslator(source='hi', target='en').translate(hindi_text)

print("Original:", hindi_text)
print("Bot Understood:", english_translation)