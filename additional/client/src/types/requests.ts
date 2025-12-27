export type RequestStatus = 'pending' | 'accepted' | 'rejected';
export type CommentAuthor = 'visiter' | 'owner';
export type RequestPriority = 'low' | 'medium' | 'high';

export interface DateTimeInfo {
    date: string;
    time_start: string;
    time_end: string;
    start_unix: number;
    end_unix: number;
}

export interface ConfirmationHistoryItem {
    confirmation_datetime: DateTimeInfo;
    occurred_at: number;
}

export interface StatusHistoryItem {
    status: RequestStatus;
    occurred_at: number;
}

export interface PriorityHistoryItem {
    priority: RequestPriority;
    occurred_at: number;
}

export interface CommentItem {
    text: string;
    author: CommentAuthor;
    created_at: number;
}

export interface ApiRequest {
    id: string;
    purpose: string;
    user_id: string;
    queue_id: string;
    preferred_datetime: DateTimeInfo;
    confirmed_datetime?: DateTimeInfo | null;
    confirmation_datetime_history: ConfirmationHistoryItem[];
    status_history: StatusHistoryItem[];
    priority_history: PriorityHistoryItem[];
    comments: CommentItem[];
    is_archived: boolean;
    priority: RequestPriority;
    status: RequestStatus;
}

export interface NormalizedRequest extends ApiRequest {
    uiStatus: 'waiting' | 'accepted' | 'archived' | 'rejected';
}

export interface ApiQueue {
    id: string;
    owner_id: string;
    name: string;
    description: string | null;
}

export interface ApiUser {
    first_name: string;
    last_name: string;
    patronymic: string | null;
}

export interface EnrichedRequest extends ApiRequest {
    queueData?: ApiQueue;
    ownerData?: ApiUser;
}
