import { useState, createContext, useContext } from 'react';

const DialogContext = createContext();

export function Dialog({ children, ...props }) {
  const [open, setOpen] = useState(false);
  
  return (
    <DialogContext.Provider value={{ open, setOpen }}>
      {children}
    </DialogContext.Provider>
  );
}

export function DialogTrigger({ children, asChild, ...props }) {
  const { setOpen } = useContext(DialogContext);
  
  if (asChild) {
    const child = children;
    return (
      <div onClick={() => setOpen(true)} {...props}>
        {child}
      </div>
    );
  }
  
  return (
    <button onClick={() => setOpen(true)} {...props}>
      {children}
    </button>
  );
}

export function DialogContent({ children, className = "", ...props }) {
  const { open, setOpen } = useContext(DialogContext);
  
  if (!open) return null;
  
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div 
        className="fixed inset-0 bg-black bg-opacity-50" 
        onClick={() => setOpen(false)}
      />
      <div 
        className={`relative bg-white rounded-lg shadow-lg p-6 w-full max-w-md mx-4 ${className}`}
        {...props}
      >
        {children}
      </div>
    </div>
  );
}

export function DialogHeader({ children, className = "", ...props }) {
  return (
    <div className={`flex flex-col space-y-1.5 text-center sm:text-left mb-4 ${className}`} {...props}>
      {children}
    </div>
  );
}

export function DialogTitle({ children, className = "", ...props }) {
  return (
    <h2 className={`text-lg font-semibold leading-none tracking-tight ${className}`} {...props}>
      {children}
    </h2>
  );
}