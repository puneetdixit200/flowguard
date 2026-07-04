#pragma once
#include <queue>
#include <mutex>
#include <condition_variable>

//thread safe bounded queue
// core producer-comsumer primitve

template<typename T>
class BlockingQueue{
public:
    explicit BlockingQueue(size_t max_size): max_size_(max_size){}

    //block if queue is full , preventing unboundd growth
    void push(T item){
        std::unique_lock<std::mutex> lock(mutex_);
        not_full_.wait(lock,[this]{return queue_.size() < max_size_ || shutdown_;});
        if(shutdown_) return;
        queue_.push(std::move(item));
        lock.unlock();
        not_empty_.notify_one();
    }
    //block if empty ,retrun false if shutdown and queue are drained

    bool pop(T& out){
        std::unique_lock<std::mutex> lock (mutex_);
        not_empty_.wait(lock,[this]{return !queue_.empty() || shutdown_;});
        if(queue_.empty())return false; //shutdown + drained
        out=std::move(queue_.front());
        queue_.pop();
        lock.unlock();
        not_full_.notify_one();
       return true;
    }

//signals all waiting threads to stop blaocking so progam can exit clean

    void shutdown(){
        std::lock_guard<std::mutex>lock(mutex_);
        shutdown_=true;
        not_empty_.notify_all();
        not_full_.notify_all();
    }
private:
    std::queue<T> queue_;
    std::mutex mutex_;
    std::condition_variable not_empty_;
    std::condition_variable not_full_;
    size_t max_size_;
    bool shutdown_=false;
};
