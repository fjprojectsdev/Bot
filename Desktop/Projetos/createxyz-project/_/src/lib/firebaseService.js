import { 
  collection, 
  addDoc, 
  getDocs, 
  doc, 
  updateDoc, 
  deleteDoc,
  query,
  where,
  orderBy,
  onSnapshot
} from 'firebase/firestore';
import { db } from './firebase.js';
import { sanitizeObject } from './sanitizer.js';

// Coleções
const PROBLEMS_COLLECTION = 'problems';
const USERS_COLLECTION = 'users';
const COMMENTS_COLLECTION = 'comments';

// Problemas
export const addProblem = async (problemData) => {
  try {
    const sanitizedData = sanitizeObject(problemData);
    const docRef = await addDoc(collection(db, PROBLEMS_COLLECTION), {
      ...sanitizedData,
      createdAt: new Date(),
      updatedAt: new Date()
    });
    return docRef.id;
  } catch (error) {
    console.error('Erro ao adicionar problema:', error);
    throw error;
  }
};

export const getProblems = async () => {
  try {
    const querySnapshot = await getDocs(
      query(collection(db, PROBLEMS_COLLECTION), orderBy('createdAt', 'desc'))
    );
    return querySnapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data()
    }));
  } catch (error) {
    console.error('Erro ao buscar problemas:', error);
    throw error;
  }
};

export const updateProblem = async (problemId, updates) => {
  try {
    const problemRef = doc(db, PROBLEMS_COLLECTION, problemId);
    await updateDoc(problemRef, {
      ...updates,
      updatedAt: new Date()
    });
  } catch (error) {
    console.error('Erro ao atualizar problema:', error);
    throw error;
  }
};

export const deleteProblem = async (problemId) => {
  try {
    await deleteDoc(doc(db, PROBLEMS_COLLECTION, problemId));
  } catch (error) {
    console.error('Erro ao deletar problema:', error);
    throw error;
  }
};

// Comentários
export const addComment = async (problemId, commentData) => {
  try {
    const sanitizedData = sanitizeObject(commentData);
    const docRef = await addDoc(collection(db, COMMENTS_COLLECTION), {
      ...sanitizedData,
      problemId,
      createdAt: new Date()
    });
    return docRef.id;
  } catch (error) {
    console.error('Erro ao adicionar comentário:', error);
    throw error;
  }
};

export const getComments = async (problemId) => {
  try {
    const q = query(
      collection(db, COMMENTS_COLLECTION),
      where('problemId', '==', problemId),
      orderBy('createdAt', 'asc')
    );
    const querySnapshot = await getDocs(q);
    return querySnapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data()
    }));
  } catch (error) {
    console.error('Erro ao buscar comentários:', error);
    throw error;
  }
};

// Listeners em tempo real
export const subscribeToProblems = (callback) => {
  const q = query(collection(db, PROBLEMS_COLLECTION), orderBy('createdAt', 'desc'));
  return onSnapshot(q, (querySnapshot) => {
    const problems = querySnapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data()
    }));
    callback(problems);
  });
};

export const subscribeToComments = (problemId, callback) => {
  const q = query(
    collection(db, COMMENTS_COLLECTION),
    where('problemId', '==', problemId),
    orderBy('createdAt', 'asc')
  );
  return onSnapshot(q, (querySnapshot) => {
    const comments = querySnapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data()
    }));
    callback(comments);
  });
};