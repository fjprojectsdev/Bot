import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

const resources = {
  pt: {
    translation: {
      problems: {
        pothole: 'Buraco na via',
        streetlight: 'Iluminação pública',
        traffic: 'Sinalização de trânsito',
        flooding: 'Alagamento'
      },
      actions: {
        add: 'Adicionar',
        edit: 'Editar',
        delete: 'Excluir',
        save: 'Salvar',
        cancel: 'Cancelar'
      },
      messages: {
        success: 'Operação realizada com sucesso',
        error: 'Erro ao realizar operação',
        loading: 'Carregando...'
      }
    }
  },
  en: {
    translation: {
      problems: {
        pothole: 'Pothole',
        streetlight: 'Street lighting',
        traffic: 'Traffic signs',
        flooding: 'Flooding'
      },
      actions: {
        add: 'Add',
        edit: 'Edit',
        delete: 'Delete',
        save: 'Save',
        cancel: 'Cancel'
      },
      messages: {
        success: 'Operation completed successfully',
        error: 'Error performing operation',
        loading: 'Loading...'
      }
    }
  }
};

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: 'pt',
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false
    }
  });

export default i18n;