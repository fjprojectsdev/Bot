import { useState, createContext, useContext } from 'react';

const SelectContext = createContext();

export function Select({ children, value, onValueChange, ...props }) {
  const [open, setOpen] = useState(false);
  const [selectedValue, setSelectedValue] = useState(value || '');
  
  const handleValueChange = (newValue) => {
    setSelectedValue(newValue);
    onValueChange?.(newValue);
    setOpen(false);
  };
  
  return (
    <SelectContext.Provider value={{ 
      open, 
      setOpen, 
      value: selectedValue, 
      onValueChange: handleValueChange 
    }}>
      <div className="relative">
        {children}
      </div>
    </SelectContext.Provider>
  );
}

export function SelectTrigger({ children, className = "", ...props }) {
  const { setOpen, open } = useContext(SelectContext);
  
  return (
    <button
      type="button"
      className={`flex h-10 w-full items-center justify-between rounded-md border border-gray-300 bg-white px-3 py-2 text-sm ring-offset-background placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 ${className}`}
      onClick={() => setOpen(!open)}
      {...props}
    >
      {children}
      <div className="ml-2">
        {open ? '▲' : '▼'}
      </div>
    </button>
  );
}

export function SelectValue({ placeholder, className = "" }) {
  const { value } = useContext(SelectContext);
  
  return (
    <span className={className}>
      {value || placeholder}
    </span>
  );
}

export function SelectContent({ children, className = "", ...props }) {
  const { open } = useContext(SelectContext);
  
  if (!open) return null;
  
  return (
    <div 
      className={`absolute top-full left-0 z-50 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg max-h-60 overflow-auto ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}

export function SelectItem({ children, value, className = "", ...props }) {
  const { onValueChange } = useContext(SelectContext);
  
  return (
    <div
      className={`cursor-pointer px-3 py-2 text-sm hover:bg-gray-100 ${className}`}
      onClick={() => onValueChange(value)}
      {...props}
    >
      {children}
    </div>
  );
}