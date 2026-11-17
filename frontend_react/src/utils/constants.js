export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';
export const APP_NAME = 'ANNASARTHI AI';
export const APP_TAGLINE = 'Good Food. Greater Purpose. Smarter Redistribution.';

// Food types
export const FOOD_TYPES = [
  'Vegetable Biryani',
  'Chicken Curry',
  'Rice',
  'Bread',
  'Dairy Dessert',
  'Other',
];

// Locations
export const LOCATIONS = [
  'Hostel Mess A',
  'Hostel Mess B',
  'Canteen',
  'Event Hall',
  'Sports Complex',
];

// Decision types
export const DECISIONS = {
  DISPATCH: { label: 'Dispatch', color: '#43865B', bg: '#E8F5E9' },
  HOLD: { label: 'Hold', color: '#D69B43', bg: '#FFF8E1' },
  DISCARD: { label: 'Discard', color: '#C65C50', bg: '#FFEBEE' },
  NO_PICKUP: { label: 'No Pickup', color: '#A0A69B', bg: '#F5F5F5' },
};

// Status types
export const STATUS_COLORS = {
  success: { color: '#43865B', bg: '#E8F5E9' },
  warning: { color: '#D69B43', bg: '#FFF8E1' },
  danger: { color: '#C65C50', bg: '#FFEBEE' },
  info: { color: '#6689A4', bg: '#E3F2FD' },
  pending: { color: '#A0A69B', bg: '#F5F5F5' },
};

// Agents
export const AGENTS = [
  { id: 'eklavya', name: 'Eklavya', role: 'Intake Agent', icon: '📥' },
  { id: 'arjuna', name: 'Arjuna', role: 'Recipient Matching', icon: '🎯' },
  { id: 'dronacharya', name: 'Dronacharya', role: 'Food Safety', icon: '🔬' },
  { id: 'chanakya', name: 'Chanakya', role: 'Coordinator', icon: '⚙️' },
];

// Chart colors
export const CHART_COLORS = {
  primary: '#3F654A',
  secondary: '#829B78',
  accent: '#C77C55',
  success: '#43865B',
  warning: '#D69B43',
  danger: '#C65C50',
};
